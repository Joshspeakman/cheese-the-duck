from concurrent.futures import Future
from types import SimpleNamespace
import pytest
from core.game import Game

def test_loading_waits_for_last_save_and_surfaces_write_failure():
    game = Game.__new__(Game)
    game._save_future = Future()
    game._save_future.set_result(False)
    with pytest.raises(IOError, match='progress'):
        game._load_game()

def test_successful_flush_and_new_game_without_a_save():
    game = Game.__new__(Game)
    game._flush_pending_save()
    game._save_future = Future()
    game._save_future.set_result(True)
    game._flush_pending_save()

def test_diary_uses_the_saved_scrapbook_photo_source():
    game = Game.__new__(Game)
    game.enhanced_diary = SimpleNamespace(get_emotion_analysis=lambda days: {}, emotion_logs=[],
                                         dreams_recorded=0, life_chapters=[], current_chapter=None)
    photo = SimpleNamespace(date_taken='2026-11-09', location='Pond', title='A duck with opinions')
    game.scrapbook = SimpleNamespace(total_photos_taken=1, photos={'one':photo})
    game.diary_manager = SimpleNamespace(get_entry_count=lambda:0, get_favorites=lambda:[])
    game._enhanced_diary_page = 0
    lines = []
    game._render_diary_overview(lines,48)
    game._render_diary_photos(lines,48,4)
    assert any('Photos:   1' in line for line in lines)
    assert any('A duck with opinio' in line for line in lines)
