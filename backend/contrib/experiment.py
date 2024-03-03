import base64
import functools
import hashlib
import json
import xml.etree.ElementTree as ET
from pathlib import Path

favicon_hashes = []


# Define a function to process each book entry
def process_book(book_elem):
    favicon_hash = hashlib.sha256(
        base64.b64decode(book_elem.attrib["favicon"])
    ).hexdigest()
    if favicon_hash not in favicon_hashes:
        favicon_hashes.append(favicon_hash)

    # book_id = book_elem.attrib['favicon']
    # book_id = book_elem.attrib['id']
    # title = book_elem.attrib['title']
    # description = book_elem.attrib.get('description', '')
    # # Process other attributes or perform additional actions as needed
    # print(f"Book ID: {book_id}, Title: {title}, Description: {description}")


favicons_path = Path("favicons")
json_library_path = Path("library.json")


def count_books():

    def count_fn(_, count):
        count[0] += 1

    count = [0]  # this is a hack to pass a mutable int
    iter_books(functools.partial(count_fn, count=count))
    print(f"{count[0]} books found")


def extract_favicons():

    favicon_hashes = []

    def extract_fn(book):
        favicon_bytes = base64.b64decode(book.attrib["favicon"])
        mime_type = book.attrib["faviconMimeType"]
        if mime_type != "image/png":
            raise ValueError(f"Unexpected favicon mime type encountered: {mime_type}")
        favicon_hash = hashlib.md5(favicon_bytes).hexdigest()
        if favicon_hash not in favicon_hashes:
            (favicons_path / f"{favicon_hash}.png").write_bytes(favicon_bytes)
            favicon_hashes.append(favicon_hash)

    favicons_path.mkdir(parents=True)
    iter_books(extract_fn)
    print(f"{len(favicon_hashes)} favicons found")


def create_json():

    dictionary = {"items": {}}

    names_overrides = {
        "los_miserables_audiobook_es": "los-miserables-audiobook_es",
        "slam-out-loud_hi_PLmQc6HNAtCsoHGzlIzzYj1SI2vWFjr_F6": "slam-out-loud_hi_PLmQc6HNAtCsoHGzlIzzYj1SI2vWFjr-F6",
        "coopmaths": "coopmaths_fr",
        "ted_en_global_issues": "ted_en_global-issues",
        "ted_countdown_global": "ted_en_countdown",
        # wikipedia: various selections with a space/underscore in selection
        "wikipedia_ar_for_schools": "wikipedia_ar_for-schools",
        "wikipedia_be-tarask_all": "wikipedia_be_all",
        "wikipedia_de_climate_change": "wikipedia_de_climate-change",
        "wikipedia_en_climate_change": "wikipedia_en_climate-change",
        "wikipedia_en_for_schools": "wikipedia_en_for-schools",
        "wikipedia_en_ice_hockey": "wikipedia_en_ice-hockey",
        "wikipedia_en_indian_cinema": "wikipedia_en_indian-cinema",
        "wikipedia_en_ray_charles": "wikipedia_en_ray-charles",
        "wikipedia_en_simple_all": "wikipedia_en_simple-all",
        "wikipedia_es_climate_change": "wikipedia_es_climate-change",
        "wikipedia_fr_climate_change": "wikipedia_fr_climate-change",
        "wikipedia_hi_indian_cinema": "wikipedia_hi_indian-cinema",
        # wikipedia: few wrong languages
        "wikipedia_map-bms_all": "wikipedia_jav_all",
        "wikipedia_nds-nl_all": "wikipedia_nds_all",
        "wikipedia_roa-tara_all": "wikipedia_roa_all",
        # wikisource: we have two websites with the zh language
        "wikisource_zh-min-nan_all": "wikisource_zh_zh",
        "wikisource_zh-min-nan_all": "wikisource_zh_zh-min-nan",
        # wiktionary
        "wiktionary_en_simple_all": "wiktionary_en_simple-words",
        # None
        "Prunelle_budding_authors_en": "prunelle_en_budding-authors",
        "Ressources_pedagogiques_relatives_au_droit_auteur": "ressource-pedagogiques-relatives-au-droit-auteur_fr_all",
        "dse_ladakh_lbj": "dse-ladakh_lbj_all",
        "la_chaine_de_maths_et_tiques_fr_all": "la-chaine-de-maths-et-tiques_fr_all",
        "prunelle_auteurs_en_herbe_fr": "prunelle_fr_budding-authors",
        "prunelle_contes_africains_fr": "prunelle_fr_african-story",
        "prunelle_draw_your_african_story_en": "prunelle_en_african-story",
        "prunelle_interactive_books_en": "prunelle_en_interactive-books",
        "prunelle_livres_interactifs_fr": "prunelle_fr_interactive-books",
        "scienceinthebath_playlist-PL8NNmkST8IoKeba_t0iMtBMYNMnV-jsTn": "scienceinthebath_en_adventures-wonders",
        "scienceinthebath_playlist-PL8NNmkST8IoIq5W5AcFy1QgD6SVGbnwrJ": "scienceinthebath_en_assorted-nonsense",
        "scienceinthebath_playlist-PL8NNmkST8IoIqO5CT11b6e9e-HJoxplPe": "scienceinthebath_en_climate-nature-environment",
        "scienceinthebath_playlist-PL8NNmkST8IoI_L0_jKSpOKpd3131yG7Tr": "scienceinthebath_en_freshest-produce",
        "scienceinthebath_playlist-PL8NNmkST8IoIpVgmaxIvzPLK7zu1xYWiD": "scienceinthebath_en_m-films",
        "scienceinthebath_playlist-PL8NNmkST8IoK6keUR5BsUspBJJBzsOE5U": "scienceinthebath_en_science-in-the-bath",
        "thaki_ar_tech_tricks": "thaki_ar_tech-tricks",
        "the_infosphere_en_all": "the-infosphere_en_all",
        "voa_learning_en_all": "voa-learning_en_all",
        "voa_learning_english-eim-english-in-a-minute": "voa-learning_en_english-in-a-minute",
        "voa_learning_english-everyday-grammar-tv": "voa-learning_en_everyday-grammar-tv",
        "voa_learning_english-how-to-pronounce": "voa-learning_en_how-to-pronounce",
        "voa_learning_english-let-s-learn-english": "voa-learning_en_let-s-learn-english-level-1",
        "voa_learning_english-let-s-learn-english-level-2": "voa-learning_en_let-s-learn-english-level-2",
        "voa_learning_english-let-s-teach-english": "voa-learning_en_let-s-teach-english",
        "voa_learning_english-news-literacy": "voa-learning_en_news-literacy",
        "voa_learning_english-word-of-the-day": "voa-learning_en_word-of-the-day",
        "madrasa_astronomy_ar_all": "madrasa-astronomy_ar_all",
        "premiers_pas_avec_python_fr": "premiers-pas-avec-python_fr_all",
    }

    ignored_book_names = [
        "kiwix.korean.stackexchange.com",
        "kiwix.portuguese.stackexchange.com",
        "gutenberg_ale_all_2022-08",
        "gutenberg_ang_all_2022-08",
        "gutenberg_bgs_all_2022-08",
        "gutenberg_brx_all_2022-07",
        "gutenberg_csb_all_2022-07",
        "gutenberg_grc_all_2022-07",
        "gutenberg_kha_all_2022-05",
        "gutenberg_kld_all_2022-08",
        "gutenberg_ko_all_2022-08",
        "gutenberg_nai_all_2022-08",
        "gutenberg_nav_all_2022-05",
        "phzh_core-arabic-one-test-zim_ar",
        "phzh_core-dari-one",
        "phzh_core-english-one_en",
        "phzh_core-greek-one_el",
        "phzh_core-italian-one_it",
        "",
    ]

    def create_fn(book):
        book_id = book.attrib["id"]

        name = book.attrib["name"]
        if name in ignored_book_names:
            return

        flavour = None
        if "flavour" in book.attrib:
            flavour = book.attrib["flavour"]

        category_tags = [
            tag
            for tag in book.attrib["tags"].split(";")
            if str(tag).startswith("_category:")
        ]
        if len(category_tags) > 1:
            print(f"Many categories found for book {book_id}")
            return
        if len(category_tags) == 0:
            category = "--"
        else:
            category = str(category_tags[0].split(":")[1])
        if category not in dictionary["items"].keys():
            dictionary["items"][category] = {"items": {}}

        if name in names_overrides:
            name = names_overrides[name]
        if category == "phet":
            parts = name.split("_")
            if parts[0] != "phets":
                print(f"Unexpected name - project - for phet book_id {book_id}: {name}")
                return
            if len(parts) > 3:
                print(f"Unexpected name length for phet book_id {book_id}: {name}")
                return
            if len(parts) == 2:
                # Ignoring old stuff which has to be cleaned up
                return
            project = parts[0]
            selection = parts[2]
            language = parts[1]
        elif category in (
            "other",
            "stack_exchange",
            "gutenberg",
            "ted",
            "wikihow",
            "wikibooks",
            "wikinews",
            "wikipedia",
            "wikiquote",
            "wikisource",
            "wikiversity",
            "wikivoyage",
            "wiktionary",
        ):
            parts = name.split("_")
            if len(parts) < 2 or len(parts) > 3:
                print(f"Unexpected name length for book_id {book_id}: {name}")
                return
            project = parts[0]
            language = parts[1]
            if len(language) > 3:
                print(f"Unexpected name - lang - for book_id {book_id}: {name}")
                return
            if len(parts) == 3:
                selection = parts[2]
            else:
                selection = "all"
        elif category == "--":
            if name.startswith("avanti-"):
                project = "avanti"
                language = "hi"
                selection = name[7:]
            elif name.startswith("maitre_lucas_"):
                project = "maitre-lucas"
                language = "fr"
                selection = name[13:-3]
            elif name.startswith("canadian_prepper_"):
                project = "canadian-prepper"
                language = "en"
                selection = name[17:-3]
            elif name.startswith("canadian_prepper_"):
                project = "canadian-prepper"
                language = "en"
                selection = name[17:-3]
            else:
                parts = name.split("_")
                if len(parts) < 2 or len(parts) > 3:
                    print(f"Unexpected name length for book_id {book_id}: {name}")
                    return
                project = parts[0]
                language = parts[1]
                if len(language) > 3:
                    print(f"Unexpected name - lang - for book_id {book_id}: {name}")
                    return
                if len(parts) == 3:
                    selection = parts[2]
                else:
                    selection = "all"

        else:
            selection = "na"
            project = "na"
            language = "na"

        dictionary["items"][category]["items"][book_id] = {
            "selection": selection,
            "language": language,
            "project": project,
            "flavour": flavour,
        }

    iter_books(create_fn)

    def count_items(a_dict):
        if "items" not in a_dict:
            return
        a_dict["count"] = len(a_dict["items"].keys())
        for value in a_dict["items"].values():
            count_items(value)

    count_items(dictionary)

    with open(json_library_path, "w") as fp:
        json.dump(dictionary, fp, indent=True)


def iter_books(func):
    with open("library_zim.xml", "rb") as f:
        context = ET.iterparse(f, events=("start", "end"))
        for event, elem in context:
            if event == "start" and elem.tag == "book":
                func(elem)
                elem.clear()
    del context


count_books()

# if not favicons_path.exists():
#     extract_favicons()
# else:
#     print("Favicons already extracted")

create_json()
# Open the XML file for streaming processing
