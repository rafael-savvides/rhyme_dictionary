# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "marimo",
#     "phyme==0.0.9",
# ]
# ///

import marimo

__generated_with = "0.15.2"
app = marimo.App(width="columns")

with app.setup:
    import marimo as mo
    from Phyme import Phyme
    from itertools import zip_longest

    ph = Phyme()


@app.cell
def _():
    mo.md(r"""# Rhyme dictionary""")
    return


@app.cell
def _():
    word_input = mo.ui.text(debounce=False, value="dog")
    word_input
    return (word_input,)


@app.cell
def _(word_input):
    word = word_input.value
    return (word,)


@app.cell
def _(get_rhymes, rhyme_select, word):
    mo.stop(word == "")

    try:
        rhymes = get_rhymes(word, rhyme_select.value)
    except KeyError:
        rhymes = {}
        print(f"No rhymes for '{word}'")
    return (rhymes,)


@app.cell
def _(rhyme_fns):
    rhyme_select = mo.ui.multiselect(
        list(rhyme_fns),
        value=["perfect", "family", "assonance", "substitution", "subtractive"],
        label="Select rhyme types: ",
    )
    rhyme_select
    return (rhyme_select,)


@app.cell
def _(rhymes, word):
    _s = (
        f"Rhymes for {word}: \n\n{concat_rhymes(rhymes)}"
        if rhymes
        else f"No rhymes for {word}."
    )

    mo.plain_text(_s)
    return


@app.cell
def _():
    rhyme_fns = {
        "additive": ph.get_additive_rhymes,
        "assonance": ph.get_assonance_rhymes,
        "consonant": ph.get_consonant_rhymes,
        "family": ph.get_family_rhymes,
        "partner": ph.get_partner_rhymes,
        "perfect": ph.get_perfect_rhymes,
        "substitution": ph.get_substitution_rhymes,
        "subtractive": ph.get_subtractive_rhymes,
    }


    def get_rhymes(
        word: str, rhyme_types: str | list[str] = ["perfect"]
    ) -> dict[str, list[str]]:
        if isinstance(rhyme_types, str):
            rhyme_types = [rhyme_types]
        rhymes = {}
        for rt in rhyme_types:
            r: dict[int, list[str]] = rhyme_fns[rt](word)
            rhymes[rt] = [w for num_syllables, words in r.items() for w in words]
        return rhymes
    return get_rhymes, rhyme_fns


@app.function
def concat_in_columns(*lists: list[str], tabs=1) -> str:
    """
    Concat lists of strings in columns.
    Example:
    concat_in_columns("a b c".split(), "1 2 3333333".split(), "232321 2 3".split(), tabs=1)
    """
    widths = [max(len(word) for word in l) for l in lists]
    s = ""
    for x in zip_longest(*lists, fillvalue=""):
        s += " ".join(f"{word:<{widths[i]}}" for i, word in enumerate(x)) + "\n"
    return s


@app.function
def concat_rhymes(rhymes: dict[str, list[str]]):
    return concat_in_columns(*[[rt, "-" * len(rt)] + r for rt, r in rhymes.items()])


if __name__ == "__main__":
    app.run()
