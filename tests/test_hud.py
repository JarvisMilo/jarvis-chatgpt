def test_hud_module_imports_without_creating_window():
    from jarvis.ui.hud import AmbientHUD
    assert AmbientHUD.__name__=="AmbientHUD"
