from acp.cli import main


def test_listprop(capsys, monkeypatch):
	monkeypatch.setattr("sys.argv", ["acp", "--listprop"])
	main()
	out = capsys.readouterr().out
	assert "Supported properties" in out
	assert "syAP" in out


def test_helpprop(capsys, monkeypatch):
	monkeypatch.setattr("sys.argv", ["acp", "--helpprop", "syAP"])
	main()
	out = capsys.readouterr().out
	assert "dec" in out
