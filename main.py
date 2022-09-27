from selenium import webdriver
from selenium.webdriver.common.by import By


class WebManipulator:

    LOGIN_URL = 'https://10.210.11.104/login'
    RESTART_URL = 'https://10.210.11.104/settings/about'
    USERNAME_INPUT = '// *[ @ id = "username"]'
    PASSWORD_INPUT = '// * [ @ id = "password"]'
    LOGIN_BUTTON = '/html/body/div[1]/div[1]/div[1]/div/form/div[6]/button'
    EXPANDER_BUTTON = '/html/body/div[1]/main/div[1]/div[2]/div/div/div[5]/button/div'
    RESTART_BUTTON = '/html/body/div[1]/main/div[1]/div[2]/div/div/div[5]/div/div/div/div[1]/button'
    CONFIRM_BUTTON = ''  # TODO: XPath for Confirm button

    # This is just to ensure we are on the correct website
    TITLE_SHOULD_CONTAIN = 'CollabOS'

    # Well sometimes it takes a while to load a page, so let's give it time
    WAIT_TIME = 4  # In seconds

    def __init__(self, username, password, dry_run=False):
        self.username = username
        self.password = password
        self.dry_run = dry_run

        # In dry-run, we hide the browser (use a headless one)
        options = webdriver.ChromeOptions()
        if not dry_run:
            options.add_argument('headless')
            # This is just problems with wrongly set meta-state for the website
            options.add_argument('window-size=1200x600')

        self.driver = webdriver.Chrome(chrome_options=options)

    def _kill(self):
        self.driver.close()

    def _login(self):
        self.driver.get(self.LOGIN_URL)
        self.driver.implicitly_wait(self.WAIT_TIME)
        assert(self.TITLE_SHOULD_CONTAIN in self.driver.title)

        # Filling inputs with credentials
        self.driver.find_element(By.XPATH, self.USERNAME_INPUT).send_keys(self.username)
        self.driver.find_element(By.XPATH, self.PASSWORD_INPUT).send_keys(self.password)

        # Login in
        self.driver.find_element(By.XPATH, self.LOGIN_BUTTON).click()

    def _restart(self):
        self.driver.get(self.RESTART_URL)
        self.driver.implicitly_wait(self.WAIT_TIME)
        assert (self.TITLE_SHOULD_CONTAIN in self.driver.title)

        # This is probably unnecessary because dropdown usually is just JS think and elements are already there
        self.driver.find_element(By.XPATH, self.EXPANDER_BUTTON).click()
        self.driver.find_element(By.XPATH, self.RESTART_BUTTON).click()
        self.driver.implicitly_wait(self.WAIT_TIME)  # Yes... let's wait
        self.driver.find_element(By.XPATH, self.CONFIRM_BUTTON).click()

    def execute(self, disable_kill=False):
        self._login()
        self._restart()

        if not disable_kill:
            self._kill()


manipulator = WebManipulator(username='', password='')
manipulator.execute()
