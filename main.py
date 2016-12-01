import mechanize
import getpass
import re
import os.path
from config import PATH

# url for login page of NU moodle. NOTE: DO NOT CHANGE
URL_login = 'https://moodle.niituniversity.in/moodle/login/index.php'

# url for page where all current course corresponding to user is present. NOTE: DO NOT CHANGE
URL_course_list_page = 'https://moodle.niituniversity.in/moodle/my/'

# regex for distinguishing course links from other links. NOTE: DO NOT CHANGE
REGEX = r"(https|http)(://)(moodle[.]niituniversity[.]in/moodle/course/view[.]php)([?]id=)(\d*)"
# regex for distinguishing file links from other links. NOTE: DO NOT CHANGE
REGEX_for_content = r"(https|http)(://)(moodle[.]niituniversity[.]in/moodle/mod/resource/view[.]php)([?]id=)(\d*)"

# opening browser
br = mechanize.Browser()

# disabling browser autorefresh
br.set_handle_refresh(False)

# adding headers to browser
br.addheaders = [('User-agent', 'Firefox')]

def login():
    # get username and password using terminal
    username = raw_input("enter username")
    password = getpass.getpass("enter password")

    try:
        # opening moodle login page
        br.open(URL_login)

        # getting 0th form which is login form
        br.form = list(br.forms())[0]

        # getting controls analogus to selecting fields to type in.
        username_control = br.form.find_control("username")
        password_control = br.form.find_control("password")

        # giving value to control analogus to filling the form
        username_control.value = username
        password_control.value = password

        # submitting the form
        response = br.submit()

        # exception handeling if password or username is wrongly entered
        if (response.geturl() == URL_login):
            print("invalid username or password")
            return False
        else:
            return True
    except:
        print("Check your internet connection!")
        return  False


# returns dictionary containing all links on page matching to regex
def return_page_dict(url, regex):
    response = br.open(url=url)
    dict = {}
    for link in br.links():
        if (re.match(regex, link.url)):
            dict[link.text] = link.url
    return dict

def main():
    try:
        while not login():
            login()
    except:
        pass

    # opening course page because presently we are on main moodle page
    try:
        dict = return_page_dict(URL_course_list_page, REGEX)

        # iterating through each subject page
        for key in dict:
            try:
                print("opening page " + key)
                br.open(url=dict[key])

                path = PATH + key
                if not os._exists(path):
                    os.makedirs(path)

                # dictionary contains all urls from which file will be downloaded
                (' \n'
                 '                NOTE: NU Moodle use PHP download scripting due to which we cannot download files directly \n'
                 '                form URL present on page\n'
                 '                ')
                dict2 = return_page_dict(dict[key], REGEX_for_content)

                # iterating through each download scripted URL
                for key2 in dict2:
                    # Trick to move behind file scripting
                    result = br.open(dict2[key2])
                    # this gives us absolute path to actual file
                    url = result.geturl()
                    #print(result.info().headers, url)

                    # downloading and saving the file
                    filename = path + '/' + key2 + '.' + os.path.splitext(url)[1]
                    print("Downloading '" + filename + "'...")
                    br.retrieve(url, filename)

            except:
                print("ERROR while opening '" + key + "' page")


    except:
        print('Oops! Something went wrong!!')

if __name__ == '__main__':
    main()