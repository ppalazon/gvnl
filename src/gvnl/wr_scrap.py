"""Extract information from Wordreference."""

import requests
from bs4 import BeautifulSoup


class Translation:
    """Wordreference translation record."""

    def __init__(self):
        """Initialize object."""
        self.expression = ""
        self.context = ""
        self.type = ""
        self.usage = ""
        self.translations = []
        self.sentences = []

    def __str__(self):
        """Use to print object information."""
        return "Translation {}[{}] -> {} ({}) {{{}}}: {}".format(
            self.expression,
            self.type,
            self.translations,
            self.context,
            self.usage,
            self.sentences,
        )


def lookup(expression):
    """Look up for an expression on Wordreference."""
    response = requests.get(
        "https://www.wordreference.com/es/translation.asp",
        params={"tranword": expression},
    )

    response.raise_for_status()

    parser = BeautifulSoup(response.text, "html.parser")

    article_wrd = parser.find("div", id="articleWRD")

    table_refs = article_wrd.find_all("table", class_="WRD")

    translations = []

    for table_ref in table_refs:
        # table_name = "Table name"
        translations_table = []
        # print(table_ref)
        for tr in table_ref.find_all("tr"):
            # class_names = tr.get("class", [])
            tr_id = tr.get("id", "")
            # if "wrtopsection" in class_names:
            #     table_name = tr.get_text()
            if "enes:" in tr_id:
                # print(tr)
                translations_table.append(Translation())
            if len(translations_table) > 0:
                new_trans = translations_table[-1]
                for td in tr.find_all("td"):
                    td_classes = td.get("class", [])
                    content = td.text.strip()
                    if content:
                        if "FrWrd" in td_classes:
                            conjugate = "".join(
                                [
                                    x.get_text()
                                    for x in td.find_all("a", class_="conjugate")
                                ]
                            ).strip()
                            trans_type = "".join(
                                [x.get_text() for x in td.find_all("em", class_="POS2")]
                            ).strip()
                            # new_trans.expression = "".join([x.get_text() for x in td.find_all('strong')])
                            new_trans.expression = (
                                content.replace(conjugate, "")
                                .replace(trans_type, "")
                                .strip()
                            )
                            new_trans.type = trans_type
                        elif "ToWrd" in td_classes:
                            conjugate = "".join(
                                [
                                    x.get_text()
                                    for x in td.find_all("a", class_="conjugate")
                                ]
                            )
                            trans_type = "".join(
                                [x.get_text() for x in td.find_all("em", class_="POS2")]
                            )
                            trans = (
                                content.replace(trans_type, "")
                                .replace(conjugate, "")
                                .strip()
                            )
                            new_trans.translations.append(trans)
                        elif "FrEx" in td_classes:
                            new_trans.sentences.append(content)
                        elif "ToEx" in td_classes:
                            pass
                        else:
                            usage = "".join(
                                [x.get_text() for x in td.find_all("i", class_="Fr2")]
                            )
                            dsense = "".join(
                                [
                                    x.get_text()
                                    for x in td.find_all("span", class_="dsense")
                                ]
                            )
                            context = (
                                content.replace(usage, "")
                                .replace(dsense, "")
                                .replace("(", "")
                                .replace(")", "")
                                .strip()
                            )
                            if usage:
                                new_trans.usage = usage
                            if context:
                                new_trans.context = context
        translations.extend(translations_table)

    return translations
    # for translation in translations:
    #     print(translation)

    # print(table_name)

    # print(table_ref.get_text())


if __name__ == "__main__":
    lookup("keen on")
