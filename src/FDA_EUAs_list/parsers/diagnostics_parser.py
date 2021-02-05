from html.parser import HTMLParser
import re

from parsers.common import get_test_id, ParserState, ParserSubState, parse_date


class DiagnosticsParser(HTMLParser):
    HEADERS = [
        "test_id",  # 0
        "Date EUA First Issued",  # 1
        "Most recent revision",  # 2
        "Entity",  # 3
        "Diagnostic name",  # 4
        "Most Recent Letter of Authorization (URL to PDF)",  # 5
        "Technology",  # 6
        "Authorized Setting(s)",  # 7
        "Fact Sheet for Healthcare Providers (HCP) (URL to PDF)",  # 8
        "Fact Sheet for Patients / Recipients (URL to PDF)",  # 9
        "Information for Use (IFU) (URL to PDF)",  # 10
        "Emergency Use Authorisation (URL to PDF)",  # 11
        "Amendments and Other Documents (PDF)",  # 12
        # "Federal Register Notice for EUA",  # 13
    ]


    def __init__(self):
        super().__init__()
        self.reset()

        self.rows = []
        self.state = ParserState.INACTIVE
        self.substate = ParserSubState.INACTIVE

        self.current_row = None
        self.current_a_tag = None
        self.current_a_tag_url = None

        self.current_row_entity_name = None
        self.current_row_test_name = None


    def handle_starttag(self, tag, attrs):
        if tag == "tbody" and self.state != ParserState.FINISHED:
            self.state = ParserState.COLLECT_ROWS

        if self.state != ParserState.COLLECT_ROWS:
            return

        self.current_a_tag = None
        self.current_a_tag_url = None

        # print("Got tag: ", tag)
        if tag == "tr":
            self.current_row = dict(zip(self.HEADERS, [""] * len(self.HEADERS)))
            # set fields which can contain multiple values
            self.current_row["Information for Use (IFU) (URL to PDF)"] = []
            self.current_row["Amendments and Other Documents (PDF)"] = []
            self.data_position = -1

        elif tag == "td":
            self.data_position += 1
            self.substate = ParserSubState.COLLECT_CELL
            self.data_subposition = 0

        elif tag == "a":
            self.current_a_tag = attrs
            self.current_a_tag_url = next(x[1] for x in self.current_a_tag if x[0] == "href")

            # Filter out this URL
            if self.current_a_tag_url == "/medical-devices/coronavirus-covid-19-and-medical-devices/sars-cov-2-reference-panel-comparative-data":
                self.current_a_tag_url = None

            elif self.current_a_tag_url.startswith("/"):
                self.current_a_tag_url = "https://www.fda.gov" + self.current_a_tag_url

        else:
            pass
            # print("Got tag: ", tag)


    def handle_endtag(self, tag):
        if self.state != ParserState.COLLECT_ROWS:
            return

        if tag == "td":
            self.substate = ParserSubState.INACTIVE

        elif tag == "tr":
            test_id = get_test_id(self.current_row_entity_name, self.current_row_test_name)
            self.current_row["test_id"] = test_id
            self.rows.append(self.current_row)
            self.current_row = None

            # temp
            # self.state = ParserState.FINISHED

        elif tag == "tbody":
            self.state = ParserState.FINISHED
            self.rows = sorted(self.rows, key=lambda row: row["Date EUA First Issued"])


    def handle_data(self, data):
        data = data.strip()

        if (self.state != ParserState.COLLECT_ROWS or
            self.substate != ParserSubState.COLLECT_CELL):
            return

        if self.data_position == 0:
            if self.current_row["Date EUA First Issued"]:
                raise Exception("Only expecting one value for date")
            self.current_row["Date EUA First Issued"] = parse_date(data)

        elif self.data_position == 1:
            if self.current_row["Most recent revision"]:
                raise Exception("Only expecting one value for most recent revision data")
            self.current_row["Most recent revision"] = parse_date(data)

        elif self.data_position == 2:
            if self.current_row["Entity"]:
                raise Exception("Only expecting one value for Entity name")
            self.current_row["Entity"] = data
            self.current_row_entity_name = data

        elif self.data_position == 3:

            if not data:
                pass
            elif not self.current_row["Diagnostic name"]:
                self.current_row["Diagnostic name"] = data
                self.current_row_test_name = data
                self.current_row["Most Recent Letter of Authorization (URL to PDF)"] = self.current_a_tag_url
            elif self.data_subposition == 1 or self.data_subposition == 2:
                pass
            else:
                raise Exception("Only expecting two or three subvalues for Test name")

            self.data_subposition += 1

        # Technology
        elif self.data_position == 4:
            if self.current_row["Technology"]:
                raise Exception("Only expecting one value for Technology")
            self.current_row["Technology"] = data

        # Authorised Settings
        elif self.data_position == 5:
            if self.current_row["Authorized Setting(s)"]:
                raise Exception("Only expecting one value for Authorised Settings")
            self.current_row["Authorized Setting(s)"] = data

        # Authorization Labeling & "extra"
        elif self.data_position == 6:
            if data == "HCP":
                if self.current_row["Fact Sheet for Healthcare Providers (HCP) (URL to PDF)"]:
                    raise Exception("Only expecting one value for HCP Fact Sheet URL")
                self.current_row["Fact Sheet for Healthcare Providers (HCP) (URL to PDF)"] = self.current_a_tag_url
            elif "Patient" in data or data == "Recipient" or data == "Recipients":
                if not self.current_row["Fact Sheet for Patients / Recipients (URL to PDF)"]:
                    self.current_row["Fact Sheet for Patients / Recipients (URL to PDF)"] = self.current_a_tag_url
                else:
                    print("Warning: multiple values for Patient / Recipients Fact Sheet URL")

            elif "IFU" in data:
                # if len(self.current_row["Information for Use (IFU) (URL to PDF)"]):
                #     print("Warning: multiple values for IFU URL for " + self.current_row["Date EUA First Issued"])
                if self.current_a_tag_url is None:
                    raise Exception("current_a_tag_url can not be None")
                self.current_row["Information for Use (IFU) (URL to PDF)"].append(self.current_a_tag_url)
                self.current_a_tag_url = None
            elif data == "EUA Summary":
                if self.current_row["Emergency Use Authorisation (URL to PDF)"]:
                    raise Exception("Only expecting one value for EUA Summary URL")
                self.current_row["Emergency Use Authorisation (URL to PDF)"] = self.current_a_tag_url
            elif "B)" in data:
                pass
            elif data:
                print("Unparsed data", data)

        # Ammendments
        elif self.data_position == 7:
            if not self.current_a_tag_url:
                if "None currently" in data or "for additional information." in data:
                    pass
                elif not data:
                    pass
                elif (
                    "reposted to include results of testing with the FDA SARS-CoV-2 Reference Panel" in data
                    or "SARS-CoV-2 Reference Panel Comparative Data" in data):
                    pass
                elif re.match("[()\s]+\d+KB", data):
                    pass
                else:
                    print("Have unexpected text for \"Amendments and Other Documents\" field: ", data)
            else:
                if "None currently" in data:
                    print("Have unexpected url in \"Amendments and Other Documents\" field: ", self.current_a_tag_url)
                elif "B)" in data:
                    pass
                elif data:
                    self.current_row["Amendments and Other Documents (PDF)"].append(self.current_a_tag_url)
                    self.current_a_tag_url = None

        elif self.data_position == 8:
            # federal register notice for EUA
            pass

        elif self.data_position == 9:
            # other brand names
            pass

        else:
            pass
            print("Encountered some data  :", self.data_position, self.current_a_tag, data)
