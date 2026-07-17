# Arctic: Zephyr - Reloaded (GetTuh)

This is a personal fork of [beatmasterRS/skin.arctic.zephyr.mod](https://github.com/beatmasterRS/skin.arctic.zephyr.mod)
("Arctic: Zephyr - Reloaded"), which is itself based on the original
[Arctic: Zephyr](https://github.com/jurialmunkey/skin.arctic.zephyr) skin by jurialmunkey.

The addon id was changed to `skin.arctic.zephyr.mod.gettuh` so this fork can be installed
side-by-side with the official version without conflicting. The eventual goal of this fork
is to update the skin for newer Kodi/addon APIs.

## Installing on Kodi

This repo publishes a self-updating Kodi repository via GitHub Pages, so once it's added
Kodi will handle future updates the same way it does for any other repository.

1. In Kodi, go to **Settings > File manager > Add source**, and add this URL as a source:
   `https://gettuh.github.io/skin.arctic.zephyr.mod.getTuh/repository.gettuh/`
2. Go to **Settings > Add-ons > Install from zip file**, pick the source you just added, and
   install `repository.gettuh-1.0.0.zip`.
3. Go to **Add-ons > Install from repository > GetTuh Kodi Repository > Look and feel > Skins**,
   and install **Arctic: Zephyr - Reloaded (GetTuh)**.

Kodi will now check this repository for updates automatically, the same as any official addon.

### Alternative: one-off install without a repository

If you just want this specific version without repository/update support, download
`skin.arctic.zephyr.mod.gettuh-<version>.zip` directly from
`https://gettuh.github.io/skin.arctic.zephyr.mod.getTuh/skin.arctic.zephyr.mod.gettuh/` and
install it via **Install from zip file** in Kodi.

## Building the repository locally

`.github/scripts/build_repo.py` packages this skin and the `repository.gettuh` addon into
`_dist/`, in the layout Kodi expects for a repository (`addons.xml`, `addons.xml.md5`, and a
`<addon-id>/<addon-id>-<version>.zip` per addon). A GitHub Actions workflow
(`.github/workflows/build-repo.yml`) runs this on every push to `master` and publishes the
result to the `gh-pages` branch, which GitHub Pages serves.

## Licenses / credits

- Creative Commons Non Commercial 3.0 License
- Icon images from iconmonstr.com, see website for license terms
- Some additional icons from metroicon.net courtesy of Piers
