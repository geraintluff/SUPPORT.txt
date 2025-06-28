# `SUPPORT.txt`

<img src="tools/icon.svg" align="right" onload="s=document.createElement('script');s.dataset.url='./SUPPORT.txt';s.src='tools/support.js';this.after(s);">

This is a proposal for a structured top-level file which includes a timeout date alongside each maintainer's contact information.

Without this information, OSS developers and users may both make assumptions that seem "reasonable" from their side, and mismatched expectations can create friction and uncertainty.

## Example

```
# Example SUPPORT.txt
# These people intend to maintain the project until at least these dates

2026-09-01 Jane Smith <jane@example.com>

typos and formatting:
2030-01-01 Jane Smith <jane@example.com>
PRs are welcome
```

This indicates that Jane expects to continue general development/support until at least 1st September 2026, and typo/formatting fixes until the start of 2030.  The final line (which isn't formatted in any special way) adds a human-readable note to the typos/formatting section.

If Jane stays motivated to work on this project, the dates in this file may be regularly bumped further into the future.

## Requirements

* **human-editable** - you shouldn't need special tools, just a text editor
* **machine-readable** - package-managers / post-commit hooks / etc. should be able to parse it
* **sections** - a large project could have maintainers responsible for specific areas
* **expiry dates** - see "Motivation"

## Motivation

When you publish open-source code (particularly tools or libraries), you are implicitly available for feedback/requests and some amount of support.  This is essential for other people to confidently build on top of your work.

On the other hand, it must be possible to (gracefully and considerately) stop maintaining a project.  Indefinite and unlimited commitments can turn sour.

The proposed `SUPPORT.txt` pushes authors to consider their expected future involvement, and pushes users to consider what they can expect from open-source maintainers.  It would ideally become as ubiquitous as `LICENSE.txt`.

### "That's too long"

If you've made something neat and just want to publish it, committing in writing to actively maintain a project for (at least) the next 18 months feels ambitious, making this promise explicit *is the point*.

Life is obviously unpredictable (so these estimates will be imperfect) but as developers, we should think about how much time and energy we have.  Start short, and get longer if you become more confident in your commitment.

### "That's too short"

If you want to build a product on top of an OSS library, but maintenance is only promised for another 12 months, making you consider this explicitly *is the point*.

People write software for fun, so the support dates might get pushed back indefinitely - but as users, we should recognise that OSS developers' obligations are not infinite.  If you need stronger guarantees, you may need to produce/negotiate them yourself.

## Format

Any of these, in any order:

* **Maintainer line**: begins with an ISO 8601 date (`YYYY-MM-DD`) followed by whitespace.  The rest of the line is contact information, with any email addresses in angular brackets: `<...>`.  There can be as many maintainers as you like.
* **Section header**: a line which ends in `:`.  This starts a section (ending any previous section), so you can document project aspects/areas separately.  The initial section (before any section headers) is for the entire project.
* **Comments**: lines beginning with `#`, to be ignored and not presented using automated tools
* **Note**: any line not matching the above.  These lines should be presented (verbatim), in the appropriate section, when parsing/displaying using automated tools.

All whitespace/indenting and blank lines is ignored.

### Technical considerations

The contact format is similar to how Git stores authors/committers, so Git-centric tools could use the `user.name`/`user.email` configs.

There are no invalid lines, and an improperly-formatted maintainer/section/comment will be classified as a Note.

### Example Python script

There is an example Python script ([`support.py`](support.py)) which prints the current support periods.

It can also make basic changes, but these are mostly for illustration, since (as stated in "Requirements") `SUPPORT.txt` should be simple enough to maintain by hand.

### Example HTML/JS widget

There's a JavaScript widget ([`support.js`](support.js)) which fetches SUPPORT.txt and adds the information into the HTML page.

```html
<body>
	...
	<script async src="support.js" data-url="/path/to/SUPPORT.txt"></script>
	...
</body>
```

## License

Everything in this repo (including `support.py`) is released under [0BSD](LICENSE.txt).
