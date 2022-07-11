# `MAINTAINERS.txt`

This is a proposal for a formatted top-level file which includes time-frames alongside each maintainer's contact information.

```
# Example MAINTAINERS.txt

2022-09-01 Jane Smith <jane@example.com>

typos and formatting:
2023-01-01 Jane Smith <jane@example.com>
```

## Motivation

When you publish open-source code (particularly tools or libraries), you implicitly make yourself available for feedback and some amount of support.  This is essential for other people to confidently build on top of your work.

On the other hand, it must be possible to (gracefully and considerately) stop maintaining a project.  Indefinite and unlimited commitments are a recipe for burnout.

The proposed `MAINTAINERS.txt` pushes maintainers to think about and document their expected future involvement.  In an actively-maintained project, this file will be periodically bumped so it remains a suitable distance in the future.

### "That's too long"

If declaring in writing that you'll actively maintain a project for at least the next 12 months feels ambitious, making this promise explicit *is the point*.

This obviously isn't binding, and life happens, but as developers we should be realistic about how much we can do in our free time.  For a new project, start short (maybe a week or a month?), and extend longer as you gain confidence in it.

### "That's too short"

If you want to build a product on top of an OSS library, but maintenance is only promised for six months, making you explicitly consider your backup plan *is the point*.

The project might well be maintained beyond this point - but if it's an important dependency, maybe you could negotiate a support plan with the maintainers, or have someone else lined up if they resign.

## Requirements

* **human-editable** - you shouldn't need special tools beyond a text editor
* **machine-readable** - package-managers should be able to parse it
* **sections** - a large project could have maintainers responsible for specific areas
* **expiry dates** - periodically refreshed as a rolling commitment when actively being maintained

## Format

There can be as many maintainers as you like.  A maintainer line begins with an ISO 8601 date, and the rest of the line is contact information, with any email addresses in angular brackets: `<...>`.

A line which ends in `:` starts a section (ending any previous section), so you can commit to only maintaining certain aspects/areas.

Comments begin with `#`, and all whitespace/indenting is ignored.

The example `MAINTAINERS.txt` above says that Jane has committed to general maintenance until at least 1st September 2022, and will also fix typos/formatting until at least the start of 2023:

### Technical considerations

The contact format is compatible with Git stores authors/committers, so automated tools could use the `user.name`/`user.email` Git configs.

There is an example Python tool (`maintainers.py`), with two commands ("bump" and "prune").

## License

Everything in this repo (including `maintainers.py`) is released under [The Unlicense](LICENSE.txt).
