# `MAINTAINERS.txt`

This is a proposal for a formatted top-level file which includes an timeout date alongside each maintainer's contact information.

```
# Example MAINTAINERS.txt
# These people will maintain the project until at least these dates

2023-09-01 Jane Smith <jane@example.com>

typos and formatting:
2024-01-01 Jane Smith <jane@example.com>
```

This indicates that Jane expects to continue general development/support until at least 1st September 2023, and typo/formatting fixes until the start of 2024.

If Jane stays motivated to work on this project, the dates in this file will be regularly bumped further into the future.

## Motivation

When you publish open-source code (particularly tools or libraries), you implicitly make yourself available for feedback and some amount of support.  This is essential for other people to confidently build on top of your work.

On the other hand, it must be possible to (gracefully and considerately) stop maintaining a project.  Indefinite and unlimited commitments are a recipe for burnout.

The proposed `MAINTAINERS.txt` pushes maintainers to think about (and document) their expected future involvement, and gives other developers clearer expectations for their dependencies.

### "That's too long"

If committing in writing to actively maintain a project for at least the next 18 months feels strange, making this promise explicit *is the point*.

This obviously isn't binding (and life happens on its own schedule) - but as developers, we should be realistic about how much time and energy we have.

### "That's too short"

If you want to build a product on top of an OSS library, but maintenance is only promised for 6 months, making you explicitly consider your backup plan *is the point*.

People write software for fun, so this date could get pushed back indefinitely - but as user-developers, we should recognise that the people who maintain our dependencies are allowed to stop.

## Requirements

* **human-editable** - you shouldn't need special tools, just a text editor
* **machine-readable** - package-managers should be able to parse it
* **sections** - a large project could have maintainers responsible for specific areas
* **expiry dates** - periodically refreshed as a rolling commitment when actively being maintained

## Format

A maintainer line begins with an ISO 8601 date, and the rest of the line is contact information, with any email addresses in angular brackets: `<...>`.  There can be as many maintainers as you like.

A line which ends in `:` starts a section (ending any previous section), so you can document certain aspects/areas separately.

Comments begin with `#`, and all whitespace/indenting is ignored.

### Technical considerations

The contact format is similar to how Git stores authors/committers, so tools could use the `user.name`/`user.email` Git configs.

There is an example Python tool (`maintainers.py`), with two commands: "bump" (update the timeout date) and "prune" (removes maintainers whose dates have passed).  However, as stated in "Requirements", `MAINTAINERS.txt` should be simple enough to maintain by hand.

## License

Everything in this repo (including `maintainers.py`) is released under [The Unlicense](LICENSE.txt).
