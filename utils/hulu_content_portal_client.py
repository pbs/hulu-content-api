from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


class HuluContentClient:
    # set timeout constant
    TIMEOUT = 20 

    # initialize client with executable path 
    def __init__(self, executable_path):
        self.executable_path=executable_path
        self.driver = None
        self.logged_in = False

        # map snakecase inputs to XPATH descriptions
        self.metric_dict = {
            "video_views": "Video_Views",
            "time_watched": "Time_Watched_Minutes",
            "viewthrough_avg": "Avg_Video_View_Thru_Percentage",
            "viewthroughs": "Video_Views_0_To_25"
        }
        self.dimesnsions_dict = {
            "content_partner": "ContentPartner",
            "series_movie": "SeriesTitle", 
            "season": "SeasonNumber",
            "package": "CPPortalPackageMapping",
            "playback_type": "BundleType",
            "asset": "VideoTitle"
        }

    # create a chromedriver instance to execute headless browsing
    def create_driver(self, headless=True):
        try:
            service = Service(self.executable_path)
            options = webdriver.ChromeOptions()
            # options.add_argument("--headless") ## SM: opens browser silently, uncomment after testing is complete
            options.add_argument("--disable-logging")
            self.driver = webdriver.Chrome(service=service,
                                           options=options)
        except Exception as e:
            raise RuntimeError(f"Error initializing ChromeDriver: {str(e)}")
        
    # close driver 
    def quit_driver(self):
        if self.driver:
            self.driver.quit() ## SM: not used yet, should 

    # wait methods
    def wait_for_presence(self, by, value, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
    
    def wait_for_clickable(self, by, value, timeout=TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
    
    # select metrics tab
    def click_metrics_tab(self):
        metrics_tab = self.wait_for_clickable(By.XPATH, "//a[text()='Metrics']")
        metrics_tab.click()

    # set filter value 
    def set_dimension(self, filter_name, values):     
        try:
            # find filter button and click 
            filter_button = self.wait_for_clickable(By.XPATH, f"//*[@id='filter-{self.dimesnsions_dict[filter_name]}']")
            filter_button.click() 

            # wait for modal to appear
            modal = self.wait_for_presence(By.CLASS_NAME, "modal-dialog")

            for value in values:
                # find dimension input field 
                input_field = modal.find_element(By.CSS_SELECTOR, ".Select-input input")
                # add value to input_field
                input_field.send_keys(value)
                # wait for dropdown to load 
                dropdown = WebDriverWait(self.driver, 120).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".Select-menu .Select-option"))
                )
                # find options and select 
                for option in dropdown:
                    if option.text == value:
                        option.click()
                        break
            # close the modal
            close_button = modal.find_element(By.CLASS_NAME, "close")
            close_button.click()

        except Exception as e:
            raise RuntimeError(f"Error setting dimension '{filter_name}': {str(e)}")

    def set_season(self, season):
        try:
            # find filter button and click 
            filter_button = self.wait_for_clickable(By.XPATH, f"//*[@id='filter-SeasonNumber']")
            filter_button.click() ## SM: need to perform click to open modal
            # wait for modal to appear
            modal = self.wait_for_presence(By.CLASS_NAME, "modal-dialog")
            # find input 
            input_field = modal.find_element(By.CSS_SELECTOR, ".react-tagsinput-input")
            # enter season 
            input_field.send_keys(season)
            # close modal 
            close_button = modal.find_element(By.CLASS_NAME, "close")
            close_button.click()

        except Exception as e:
            raise RuntimeError(f"Error setting season:{str(e)}")


    # select metric to view 
    def set_metric(self, metric):
        try:
            xpath_id = f"//button[@id='report-type-{self.metric_dict[metric]}']"
            metric_button = self.wait_for_presence(By.XPATH, xpath_id)
            metric_button.click()
        except Exception as e:
            raise RuntimeError(f"Error setting metric '{metric}': {str(e)}")

    # set time intrement 
    def set_time_increment(self, time_increment):
        try:
            time_increment_dropdown = self.wait_for_clickable(By.XPATH, "//div[@class='Select-control']")
            time_increment_dropdown.click()

            xpath_id = f"//div[@class='Select-menu-outer']//div[text()='{time_increment.capitalize()}']"
            time_inrement_option = self.wait_for_clickable(By.XPATH, xpath_id)
            time_inrement_option.click()
        except Exception as e:
            raise RuntimeError(f"Error setting time increment: {str(e)}")

    # set date range 
    def set_date_range(self, start_date, end_date):
        try:
            start_date_input = self.wait_for_clickable(By.XPATH, "//input[@placeholder='Start Date']")
            end_date_input = self.wait_for_clickable(By.XPATH, "//input[@placeholder='End Date']")
            
            start_date_input.send_keys(start_date)
            end_date_input.send_keys(end_date)
        except Exception as e:
            raise RuntimeError(f"Error setting date range: {str(e)}")

    
    # ------ LOGIN LOGIC ------ #
    def login(self, email, password):
        try:
            if not self.driver:
                self.create_driver()

                if not self.logged_in:
                    login_url = "https://content.hulu.com/login"
                    self.driver.get(login_url)

                    email_input = self.wait_for_presence(By.XPATH, "//input[@aria-required='true'][@id='email']")
                    password_input = self.wait_for_presence(By.XPATH, "//input[@aria-required='true'][@id='password']")

                    email_input.send_keys(email)
                    password_input.send_keys(password)

                    login_button = self.wait_for_presence(By.CSS_SELECTOR, ".ant-btn-primary")
                    login_button.click()

                    self.logged_in = True
                
                else:
                    print("Already logged in!")
        except Exception as e:
            raise RuntimeError(f"Error during login: {str(e)}")

    # ------ METRICS LOGIC ------ #
    def get_metrics(self, metric, content_partner, series_movie, season, package, playback_type,
                    asset, time_increment, start_date, end_date):
        try:
            if not self.driver:
                print("No browser. Create a browser instanve before proceeding")
                return
            if not self.logged_in:
                self.login()

            # select metrics tab
            self.click_metrics_tab()
            
            # select metric to view
            self.set_metric(metric)

            ## SM: hold for dimensions logic -- need a way to get a list of dropdown options
            self.set_dimension("content_partner", content_partner)
            self.set_dimension("series_movie", series_movie)
            self.set_season(season)
            self.set_dimension("package", package)
            self.set_dimension("playback_type", playback_type)

            # set date range paramters 
            self.set_time_increment(time_increment)
            self.set_date_range(start_date, end_date)

            # find submit button
            submit_button = self.driver.find_element(By.ID, "gen-report-btn")
            submit_button.click()
            # return success message
        except Exception as e:
            raise RuntimeError(f"Error fetching metrics: {str(e)}")