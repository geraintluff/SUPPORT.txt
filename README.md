# `SUPPORT.txt`

This is a proposal for a structured top-level file which includes a timeout date alongside each maintainer's contact information.

Without this information, OSS developers and users may both make assumptions that seem "reasonable" from their side, and mismatched expectations can create friction and uncertainty.

## Example

```
# Example SUPPORT.txt
# These people will maintain the project until at least these dates

2023-09-01 Jane Smith <jane@example.com>

typos and formatting:
2024-01-01 Jane Smith <jane@example.com>
```

This indicates that Jane expects to continue general development/support until at least 1st September 2023, and typo/formatting fixes until the start of 2024.

If Jane stays motivated to work on this project, the dates in this file may be regularly bumped further into the future.

## Requirements

* **human-editable** - you shouldn't need special tools, just a text editor
* **machine-readable** - package-managers should be able to parse it
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

If you want to build a product on top of an OSS library, but maintenance is only promised for 6 months, making you consider this explicitly *is the point*.

People write software for fun, so the support dates might get pushed back indefinitely - but as users, we should recognise that OSS developers' obligations are not infinite.  If you need stronger guarantees, you may need to produce/negotiate them yourself.

## Format

A maintainer line begins with an ISO 8601 date (`YYYY-MM-DD`) followed by whitespace, and the rest of the line is contact information, with any email addresses in angular brackets: `<...>`.  There can be as many maintainers as you like.

A line which ends in `:` starts a section (ending any previous section), so you can document certain aspects/areas separately.

Comments begin with `#`.  All whitespace/indenting is ignored.

### Technical considerations

The contact format is similar to how Git stores authors/committers, so Git-centric tools could use the `user.name`/`user.email` configs.

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
