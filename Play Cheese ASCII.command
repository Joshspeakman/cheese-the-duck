#!/bin/zsh
set -e
cheese_port_dir="$(cd -- "$(dirname -- "$0")" && pwd)"
open "$cheese_port_dir/engine/dist/mac-arm64/Cheese the Duck ASCII Engine.app"
