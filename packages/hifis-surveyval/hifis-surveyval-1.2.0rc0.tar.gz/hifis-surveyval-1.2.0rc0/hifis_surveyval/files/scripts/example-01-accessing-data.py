# hifis-surveyval
# Framework to help developing analysis scripts for the HIFIS Software survey.
#
# SPDX-FileCopyrightText: 2021 HIFIS Software <support@hifis.net>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""This example script demonstrates accessing metadata and data of a survey."""
from pathlib import Path

from hifis_surveyval.data_container import DataContainer
from hifis_surveyval.hifis_surveyval import HIFISSurveyval


def run(hifis_surveyval: HIFISSurveyval, data: DataContainer):
    """
    Execute example script that illustrates how to access metadata and data.

    This script in one of a series of example scripts. These examples
    demonstrate the API of the HIFIS-Surveyval Framework. They illustrate the
    process of retrieving data, manipulating data and finally plotting data.

    This particular script is about accessing metadata and data of a survey.

    Please note that the HIFIS-Surveyval Framework does not replace data
    analysis libraries like _Pandas_ which is heavily used for data analysis
    tasks that arise in a survey analysis. In order to dive into the use cases
    and benefits of Pandas you can find a lot of learning material online and
    on the Pandas webpage: https://pandas.pydata.org/
    """
    print("Example analysis script name: " + Path(__file__).stem)

    ###
    # The DataContainer can be used to retrieve a QuestionCollection object by
    # providing an ID.
    #
    # QuestionCollections, Questions and AnswerOptions have IDs. As in the
    # examples below they can be used to query for those objects. The IDs are
    # taken from the metadata and correspond to the header of the CSV file
    # with the survey answers.
    #
    # Since we are using a tool called LimeSurvey to conduct surveys it is by
    # convention that the ID of a QuestionCollection starts with the letter
    # "Q", the ID of a Question with the letters "SQ" and the ID of an
    # AnswerOption with letter "A". These letters are followed by three digits
    # to give it an unique number, e.g. "Q001". This naming convention is the
    # default of LimeSurvey, but you can use any unique IDs that fit your
    # needs.
    #
    # A QuestionCollection is a set of questions that have the same context and
    # refer to the same topic. A QuestionCollection always consists of at least
    # one Question object. There are no empty QuestionCollection objects.
    ###
    collection_topic_center = data.collection_for_id("Q001")
    print("1) ===== Get a QuestionCollection =====")
    hifis_surveyval.printer.pretty_print(collection_topic_center)

    ###
    # Once a QuestionCollection object is at hand the full ID can be retrieved.
    ###
    collection_full_id = collection_topic_center.full_id
    print("2) ===== ID of a QuestionCollection =====")
    hifis_surveyval.printer.pretty_print(collection_full_id)

    ###
    # A text of a QuestionCollection can be translated into different supported
    # languages specified by an IETF language tag which consists of the ISO
    # 693-1 two-letter language codes and a two-letter region specifier
    # concatenated by a dash. These translations are given in the metadata.
    ###
    collection_text = collection_topic_center._text.get_translation("en-GB")
    print("3) ===== Translated text of a QuestionCollection =====")
    hifis_surveyval.printer.pretty_print(collection_text)

    ###
    # A text of a QuestionCollection can also be represented by its label
    # in cases where the full translation of the title is too long and not
    # concise enough.
    ###
    collection_label = collection_topic_center._label
    print("4) ===== Label of a QuestionCollection =====")
    hifis_surveyval.printer.pretty_print(collection_label)

    ###
    # The DataContainer can be used to retrieve a Question object by providing
    # an ID. By convention the ID of a Question starts with the letters "SQ"
    # followed by three digits to give it a number, e.g. "SQ001". A Question is
    # one of the Questions in a QuestionCollection. A Question always belongs
    # to a QuestionCollection. Due to this relation between Questions and
    # QuestionCollections we need to provide both IDs separated by a so called
    # HIERARCHY_SEPARATOR which is the character "/" by default, e.g.
    # "Q001/SQ001".
    ###
    question_choose_center = data.question_for_id("Q001/_")
    print("5) ===== Get a Question =====")
    hifis_surveyval.printer.pretty_print(question_choose_center)

    ###
    # Given a Question object the full ID can be retrieved.
    ###
    question_full_id = question_choose_center.full_id
    print("6) ===== ID of a Question =====")
    hifis_surveyval.printer.pretty_print(question_full_id)

    ###
    # A text of a Question can also be translated into different supported
    # languages specified by the ISO 693-1 two-letter language codes.
    ###
    question_text = question_choose_center._text.get_translation("en-GB")
    print("7) ===== Translated text of a Question =====")
    hifis_surveyval.printer.pretty_print(question_text)

    ###
    # A text of a Question can also be represented by its label in cases where
    # the full translation of the title is too long and not concise enough.
    ###
    question_label = question_choose_center._label
    print("8) ===== Label of a Question =====")
    hifis_surveyval.printer.pretty_print(question_label)

    ###
    # In the context of a QuestionCollection object you can also retrieve
    # specific Question objects. Because of the unambiguity the ID can be
    # shorter leaving out the ID part of the QuestionCollection.
    ###
    question_choose_center = collection_topic_center.question_for_id("_")
    print("9) ===== Get a Question from a QuestionCollection =====")
    hifis_surveyval.printer.pretty_print(question_choose_center)

    ###
    # AnswerOption objects are the answers that can be given by survey
    # participants to a particular Question. They are the actual data
    # collected by a survey. AnswerOptions are identified by an ID that
    # consists of the letter "A" and three digits to give each AnswerOption
    # a number, e.g. "A001".
    ###
    answer_option = question_choose_center._answer_options["A001"]
    print("10) ===== Get an AnswerOption from a Question =====")
    hifis_surveyval.printer.pretty_print(answer_option)

    ###
    # Based on an AnswerOption object the full ID can be retrieved which is
    # made up of a Question ID and an AnswerOption ID separated by the
    # HIERARCHY_SEPARATOR, e.g. "SQ001/A001".
    ###
    answer_option_full_id = answer_option.full_id
    print("11) ===== ID of an AnswerOption =====")
    hifis_surveyval.printer.pretty_print(answer_option_full_id)

    ###
    # A text of an AnswerOption can also be translated into different supported
    # languages specified by the ISO 693-1 two-letter language codes.
    ###
    answer_option_text = answer_option._text.get_translation("en-GB")
    print("12) ===== Translated text of an AnswerOption =====")
    hifis_surveyval.printer.pretty_print(answer_option_text)

    ###
    # A text of an AnswerOption can also be represented by its label
    # in cases where the full translation of the title is too long and not
    # concise enough.
    ###
    answer_option_label = answer_option._label
    print("13) ===== Label of an AnswerOption =====")
    hifis_surveyval.printer.pretty_print(answer_option_label)

    ###
    # Accessing data/answers of a Question given by survey participants can be
    # done by the participant ID/row-index. Please note that these IDs/indices
    # are non-continuous.
    ###
    given_answer = question_choose_center.answers["1"]
    print("14) ===== Access given answers =====")
    hifis_surveyval.printer.pretty_print(given_answer)

    ###
    # A DataFrame object is a table-like data structure with header columns,
    # indexed rows and cells taking up the actual data. The DataFrame data
    # structure is provided by Pandas - a data analysis library. It is meant
    # as a base format in this survey analysis framework and is therefore
    # heavily used by it. In order to get a DataFrame object the DataContainer
    # object offers a method to do so. As an argument the method accepts a
    # list of QuestionCollection IDs. The resulting DataFrame object contains
    # as many columns as there are Questions in the selected
    # QuestionCollections and each cell contains an answer to a Question.
    ###
    dataframe_center = data.data_frame_for_ids(["Q001", "Q002"])
    print("15) ===== DataFrame of QuestionCollections =====")
    hifis_surveyval.printer.print_dataframe(dataframe_center)

    ###
    # Another way to get a DataFrame of a specific QuestionCollection is to
    # use the respective method offered by a QuestionCollection object.
    ####
    dataframe_center = collection_topic_center.as_data_frame()
    print("16) ===== DataFrame of a QuestionCollection =====")
    hifis_surveyval.printer.print_dataframe(dataframe_center)

    ###
    # Pandas also provides a table-like data structure with only one column
    # which is called Series.
    ###
    series_chosen_center = question_choose_center.as_series()
    print("17) ===== Series of a Question =====")
    hifis_surveyval.printer.print_dataframe(series_chosen_center)
