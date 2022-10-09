from selenium import webdriver
from selenium.webdriver.common.by import By


class WebManipulator:
    LOGIN_URL = 'https://{}/login'
    RESTART_URL = 'https://{}/settings/about'
    USERNAME_INPUT = '// *[ @ id = "username"]'
    PASSWORD_INPUT = '// * [ @ id = "password"]'
    LOGIN_BUTTON = '/html/body/div[1]/div[1]/div[1]/div/form/div[6]/button'
    EXPANDER_BUTTON = '/html/body/div[1]/main/div[1]/div[2]/div/div/div[5]/button/div'
    RESTART_BUTTON = '/html/body/div[1]/main/div[1]/div[2]/div/div/div[5]/div/div/div/div[1]/button'
    CONFIRM_BUTTON = '/html/body/div[1]/main/div[1]/div[2]/div/div/div[5]/div/div/div/div[1]/div/div[2]/div[2]/div[' \
                     '3]/button[1] '

    # This is just to ensure we are on the correct website
    TITLE_SHOULD_CONTAIN = 'CollabOS'

    # Well sometimes it takes a while to load a page, so let's give it time
    WAIT_TIME = 5  # In seconds

    def __init__(self, username, password, ip, dry_run=False):
        self.username = username
        self.ip = ip
        self.password = password
        self.dry_run = dry_run

        # In dry-run, we hide the browser (use a headless one)
        options = webdriver.ChromeOptions()
        options.add_argument('ignore-certificate-errors')
        if not self.dry_run:
            options.add_argument('headless')
            # This is just problems with wrongly set meta-state for the website
            options.add_argument('window-size=1200x600')

        self.driver = webdriver.Chrome(chrome_options=options)

    def _kill(self):
        self.driver.close()

    def _login(self):
        self.driver.get(self.LOGIN_URL.format(self.ip))
        self.driver.implicitly_wait(self.WAIT_TIME)
        assert (self.TITLE_SHOULD_CONTAIN in self.driver.title)

        # Filling inputs with credentials
        self.driver.find_element(By.XPATH, self.USERNAME_INPUT).send_keys(self.username)
        self.driver.find_element(By.XPATH, self.PASSWORD_INPUT).send_keys(self.password)

        # Login in
        self.driver.find_element(By.XPATH, self.LOGIN_BUTTON).click()

    def _restart(self):
        self.driver.get(self.RESTART_URL.format(self.ip))
        self.driver.implicitly_wait(self.WAIT_TIME)
        assert (self.TITLE_SHOULD_CONTAIN in self.driver.title)

        # This is probably unnecessary because dropdown usually is just JS think and elements are already there
        self.driver.find_element(By.XPATH, self.EXPANDER_BUTTON).click()
        self.driver.implicitly_wait(self.WAIT_TIME)
        self.driver.find_element(By.XPATH, self.RESTART_BUTTON).click()
        self.driver.implicitly_wait(self.WAIT_TIME)  # Yes... let's wait
        if not self.dry_run:
            self.driver.find_element(By.XPATH, self.CONFIRM_BUTTON).click()

    def execute(self, disable_kill=False):
        self._login()
        while 'login' in self.driver.current_url:
            pass  # We will be waiting for the page to load

        self._restart()
        self.driver.implicitly_wait(self.WAIT_TIME)

        if not disable_kill:
            self._kill()


# Only part which you should modify :)
manipulator = WebManipulator(username='', password='', ip='', dry_run=False)
manipulator.execute()  # Let's run the scraper
