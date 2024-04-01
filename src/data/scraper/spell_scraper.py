import os
import json
import time
import requests

from bs4 import BeautifulSoup

from src import RAW_DATA_DIR

os.environ['PYTHONIOENCODING'] = 'utf-8'

ROOT_URL = 'https://www.dandwiki.com'


def get_spells_from_main_spell_page(href):

    main_spell_page_html = get_main_spell_page_html(href)
    spell_links = main_spell_page_html.find_all("ul")

    # this is due to a weird formatting in the page
    for i in [0, 1]:
        for spell_link in spell_links[i].find_all('li'):

            spell_link = spell_link.next

            print("-" * 24)
            print(spell_link.attrs['href'])

            spell_dict = get_spell(spell_link.attrs['href'], spell_link.text.replace('\n', '').strip())

            if spell_dict:
                yield spell_dict

            print("-" * 24)

            time.sleep(5)


def get_main_spell_page_html(href):

    main_page_url = f"{ROOT_URL}/{href}"

    html = requests.get(main_page_url, headers={'User-Agent': 'Mozilla/5.0'}).content
    htmlParse = BeautifulSoup(html, 'html.parser')

    return htmlParse


def get_spell(href, spell_name):

    spell_url = f"{ROOT_URL}/{href}"

    try:

        spell_html = requests.get(spell_url, headers={'User-Agent': 'Mozilla/5.0'}).content
        spell_htmlParse = BeautifulSoup(spell_html, 'html.parser')
        spell_features_html = spell_htmlParse.find_all('tr')

        if len(spell_features_html) == 0:
            return None
        
        spell_features = {}
        spell_features['spell_url'] = spell_url
        spell_features['spell_name'] = spell_name

        for i, spell_feature in enumerate(spell_features_html):
                            
            if 'casting_time' in spell_features and 'range' in spell_features and 'duration' in spell_features:
                break
            
            if i == 0:
                spell_features['header'] = spell_feature.text.replace('\n', '').strip()
            else:
                
                spell_html_feature_name = spell_feature.find('th')

                if spell_html_feature_name:
                    spell_feature_name = spell_html_feature_name.text.replace(':\n', '').replace(' ', '_').strip().lower()
                else:
                    continue
                
                spell_feature_value = spell_feature.find('td').text

                if spell_feature_value[-1] == '\n':
                    spell_feature_value = spell_feature_value[:-1]
                
                spell_feature_value = spell_feature_value.strip()

                if spell_feature_name != 'casting_time' and spell_feature_name != 'range' and spell_feature_name != 'components' and spell_feature_name != 'duration':
                    spell_features['others'] = spell_feature_value
                else:
                    spell_features[spell_feature_name] = spell_feature_value

        spell_table_description = spell_htmlParse.find('table', {'class': "d20 dragon monstats"})
        end_description = spell_htmlParse.find('hr')

        spell_description = ""

        for sibling in spell_table_description.next_siblings:
            if sibling == end_description:
                break
            text = sibling.get_text()
            if text:
                spell_description += text
                spell_description = spell_description.strip() + "\n"

        # remove last new line character
        spell_description = spell_description[:-1]
        spell_features['description'] = spell_description

        spell_classes_html = spell_htmlParse.find_all('a', {'href': "/wiki/5e_Spells"})
        spell_classes = [x.next_sibling.next_sibling.text for x in spell_classes_html]
        spell_features['classes'] = spell_classes

    except Exception as e:
        
        print(f"ERROR!!! {e}")
        return None

    return spell_features


def main():
    
    output_file_path = os.path.join(RAW_DATA_DIR, 'spells_homebrew.jsonl')

    with open(output_file_path, 'w', encoding='utf8') as f:

        for message in get_spells_from_main_spell_page('wiki/5e_All_Spells'):
            json.dump(message, f)
            f.write('\n')


if __name__ == "__main__":
    main()
