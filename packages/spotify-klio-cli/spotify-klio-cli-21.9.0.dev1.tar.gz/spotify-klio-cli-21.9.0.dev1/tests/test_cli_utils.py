# Copyright 2020 Spotify AB

import sys

import pytest

from spotify_klio_cli import cli_utils


@pytest.mark.parametrize("filename", (None, "-", "input.txt"))
def test_smart_open(filename, mocker):
    m_open = mocker.mock_open()
    mock_open = mocker.patch("spotify_klio_cli.cli_utils.open", m_open)

    with cli_utils.smart_open(filename, fmode="r") as act_ret:
        pass

    if filename and filename != "-":
        mock_open.assert_called_once_with(filename, "r")
        assert act_ret.closed
    else:
        mock_open.assert_not_called()
        assert act_ret == sys.stdout


@pytest.mark.parametrize("has_executor", (True, False))
def test_has_internal_executor(has_executor, mocker, monkeypatch):
    package = "klio-exec"
    if has_executor:
        package = "spotify-klio-exec"

    dockerfile = (
        '## -*- docker-image-name: "gcr.io/foo/bar" -*-\n'
        "FROM my-image:1.2.3\n"
        "RUN pip install {package}\n"
    ).format(package=package)
    m_open = mocker.mock_open(read_data=dockerfile)
    mock_open = mocker.patch("spotify_klio_cli.cli_utils.open", m_open)

    mock_click_confirm = mocker.Mock()
    monkeypatch.setattr(cli_utils.click, "confirm", mock_click_confirm)

    cli_utils.has_internal_executor("job-dir")

    mock_open.assert_called_once_with("job-dir/Dockerfile", "r")
    if not has_executor:
        assert 1 == mock_click_confirm.call_count
    else:
        mock_click_confirm.assert_not_called()
