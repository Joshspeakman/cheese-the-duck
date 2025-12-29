#!/usr/bin/env python3
"""
Memory monitoring script for Stupid Duck game.
Tracks memory usage over time to detect leaks.
"""
import psutil
import time
import sys
from datetime import datetime

def monitor_process(pid, duration_minutes=5, interval_seconds=10):
    """
    Monitor memory usage of a process.

    Args:
        pid: Process ID to monitor
        duration_minutes: How long to monitor (minutes)
        interval_seconds: Sampling interval (seconds)
    """
    try:
        process = psutil.Process(pid)
    except psutil.NoSuchProcess:
        print(f"Error: No process found with PID {pid}")
        return

    print(f"Monitoring process {pid} ({process.name()}) for {duration_minutes} minutes...")
    print(f"Sampling every {interval_seconds} seconds")
    print("-" * 80)
    print(f"{'Time':<20} {'RSS (MB)':<15} {'VMS (MB)':<15} {'% Memory':<15}")
    print("-" * 80)

    start_time = time.time()
    end_time = start_time + (duration_minutes * 60)

    samples = []

    try:
        while time.time() < end_time:
            try:
                # Get memory info
                mem_info = process.memory_info()
                mem_percent = process.memory_percent()

                # RSS = Resident Set Size (actual physical memory)
                # VMS = Virtual Memory Size (total memory including swap)
                rss_mb = mem_info.rss / 1024 / 1024
                vms_mb = mem_info.vms / 1024 / 1024

                timestamp = datetime.now().strftime("%H:%M:%S")

                print(f"{timestamp:<20} {rss_mb:<15.2f} {vms_mb:<15.2f} {mem_percent:<15.2f}")

                samples.append({
                    'time': time.time() - start_time,
                    'rss': rss_mb,
                    'vms': vms_mb,
                    'percent': mem_percent
                })

                time.sleep(interval_seconds)

            except psutil.NoSuchProcess:
                print("\nProcess terminated.")
                break

    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")

    # Analysis
    if len(samples) > 1:
        print("\n" + "=" * 80)
        print("ANALYSIS")
        print("=" * 80)

        first_sample = samples[0]
        last_sample = samples[-1]

        rss_change = last_sample['rss'] - first_sample['rss']
        vms_change = last_sample['vms'] - first_sample['vms']

        print(f"Duration: {(last_sample['time'] / 60):.2f} minutes")
        print(f"Samples collected: {len(samples)}")
        print(f"\nMemory Change:")
        print(f"  RSS: {first_sample['rss']:.2f} MB -> {last_sample['rss']:.2f} MB ({rss_change:+.2f} MB)")
        print(f"  VMS: {first_sample['vms']:.2f} MB -> {last_sample['vms']:.2f} MB ({vms_change:+.2f} MB)")

        # Calculate average growth rate
        if len(samples) > 2:
            time_diff = last_sample['time'] - first_sample['time']
            growth_rate_mb_per_min = (rss_change / time_diff) * 60

            print(f"\nGrowth Rate: {growth_rate_mb_per_min:+.2f} MB/minute")

            # Detect potential leak
            if growth_rate_mb_per_min > 1.0:  # More than 1 MB per minute
                print("\n⚠️  WARNING: Potential memory leak detected!")
                print(f"   Memory is growing at {growth_rate_mb_per_min:.2f} MB/minute")
            elif growth_rate_mb_per_min > 0.5:
                print("\n⚠️  NOTICE: Gradual memory growth observed")
                print(f"   Memory is growing at {growth_rate_mb_per_min:.2f} MB/minute")
            else:
                print("\n✅ Memory usage appears stable")

        # Check for monotonic increase (never decreases = likely leak)
        increases = 0
        decreases = 0
        for i in range(1, len(samples)):
            if samples[i]['rss'] > samples[i-1]['rss']:
                increases += 1
            elif samples[i]['rss'] < samples[i-1]['rss']:
                decreases += 1

        if increases > 0 and decreases == 0:
            print(f"\n⚠️  Memory ONLY increased ({increases} times, 0 decreases)")
            print("   This suggests a memory leak pattern")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python monitor_memory.py <PID> [duration_minutes] [interval_seconds]")
        print("\nTo find the game PID:")
        print("  1. Start the game")
        print("  2. In another terminal run: ps aux | grep python | grep main.py")
        print("  3. Use the PID from the second column")
        sys.exit(1)

    pid = int(sys.argv[1])
    duration = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    interval = int(sys.argv[3]) if len(sys.argv) > 3 else 10

    monitor_process(pid, duration, interval)
