from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.utils import get_color_from_hex
from kivy.core.window import Window

# Constants
SOLAR_PANEL_EFFICIENCY = 0.15
COST_PER_UNIT_CURRENT_INR = 30000
WATT_PER_SQUARE_METER = 150
GRID_EMISSIONS_FACTOR = 0.6
CO2_ABSORBED_PER_TREE_PER_YEAR = 22.6

# Initialize area_required_sqft as None
area_required_sqft = None

class MainPage(Screen):
    def __init__(self, **kwargs):
        super(MainPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.units_label = Label(text="Enter your average monthly electricity consumption (units of current):")
        self.layout.add_widget(self.units_label)

        self.units_entry = TextInput(multiline=False)
        self.layout.add_widget(self.units_entry)

        self.calculate_button = Button(text="Calculate", size_hint=(None, None), size=(100, 40))
        self.calculate_button.bind(on_press=self.calculate_solar_energy)
        self.layout.add_widget(self.calculate_button)

        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)

        self.next_button = Button(text="Next", size_hint=(None, None), size=(100, 40))
        self.next_button.bind(on_press=self.next_page)
        self.layout.add_widget(self.next_button)

        self.add_widget(self.layout)

    def calculate_solar_energy(self, instance):
        global area_required_sqft

        current_units = float(self.units_entry.text)

        #battery_storage_kWh = current_units

        solar_power_required = round(current_units / 100,0)

        solar_panels_required = solar_power_required * 2

        area_required_sqft = solar_power_required * 100

        total_cost_inr = solar_panels_required * 15000

        if solar_power_required <= 3:
            total_cost = 70000 * solar_power_required
        else:
            total_cost = 65000 * solar_power_required

        total_cost = total_cost + total_cost * 0.12 + 12000 

        electric_bill = 0
        if current_units < 200:
            electric_bill = current_units * 8
        else:
            electric_bill = (current_units - 200) * 8.5 + 200 * 8

        bill_reduction = electric_bill * 1.2

        extra_income = (solar_power_required * 120 - current_units) * 4.5

        self.result_label.text = (f"Min.Estimated Area Required: {area_required_sqft:.2f} square feet\n"
                                  f"Solar Panels Required: {solar_panels_required:.2f} Panels\n\n"
                                   f"Total Cost of Solar Panels: Rs.{total_cost_inr:.2f}\n"
                                   f"Solar power required: {solar_power_required} kW\n" 
                                   f"Total project Cost: Rs.{total_cost}\nThis Cost includes Panels, Installation, Invertor, 12% gst and bescom charges\n"
                                   f"Estimated Monthly Electric Bill reduction: Rs.{bill_reduction:.2f}\n"
                                   f"Bill payable: Rs.0\n"
                                   f"Units generated(per month): {solar_power_required * 120}\n"
                                   f"Extra Income: Rs.{extra_income}\n" 
                                   f"Please click 'Next' to enter the number of sunlight hours per day:")

    def next_page(self, instance):
        self.manager.get_screen('sunlight_page').clear_input_fields()
        self.manager.current = 'sunlight_page'

class SunlightPage(Screen):
    def __init__(self, **kwargs):
        super(SunlightPage, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        self.sunlight_hours_label = Label(text="Number of sunlight hours per day:")
        self.layout.add_widget(self.sunlight_hours_label)

        self.sunlight_hours_entry = TextInput(multiline=False)
        self.layout.add_widget(self.sunlight_hours_entry)

        self.calculate_sunlight_button = Button(text="Calculate Solar Energy Production", size_hint=(None, None), size=(420, 40))
        self.calculate_sunlight_button.bind(on_press=self.calculate_solar_energy_with_sunlight_hours)
        self.layout.add_widget(self.calculate_sunlight_button)

        self.result_label_2 = Label(text="")
        self.layout.add_widget(self.result_label_2)

        self.back_button = Button(text="Back", size_hint=(None, None), size=(100, 40))
        self.back_button.bind(on_press=self.back_to_main)
        self.layout.add_widget(self.back_button)

        self.add_widget(self.layout)

    def calculate_solar_energy_with_sunlight_hours(self, instance):
        global area_required_sqft

        sunlight_hours_per_day = float(self.sunlight_hours_entry.text)

        solar_energy_production = area_required_sqft * sunlight_hours_per_day * SOLAR_PANEL_EFFICIENCY

        co2_reduction = solar_energy_production * GRID_EMISSIONS_FACTOR

        trees_saved = co2_reduction / CO2_ABSORBED_PER_TREE_PER_YEAR

        new_output = (f"\nSunlight Hours per Day: {sunlight_hours_per_day:.2f}\n"
                      f"Solar Energy Production: {solar_energy_production:.2f} kWh per day\n"
                      f"Estimated CO2 Emissions Reduction: {co2_reduction:.2f} kg CO2 per day\n"
                      f"Estimated Number of Trees Saved: {trees_saved:.2f} trees per day")
        self.result_label_2.text = new_output

    def back_to_main(self, instance):
        self.manager.current = 'main_page'

    def clear_input_fields(self):
        self.sunlight_hours_entry.text = ""
        self.result_label_2.text = ""

class SolarEnergyCalculatorApp(App):

    def build(self):
        self.title = "Solar Energy Calculator"
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=10)

        # Set the background color to dark grey
        Window.clearcolor = (0.05, 0.05, 0.1, 2)  # Dark grey color in RGBA format

        self.sm = ScreenManager()

        main_page = MainPage(name='main_page')
        sunlight_page = SunlightPage(name='sunlight_page')

        self.sm.add_widget(main_page)
        self.sm.add_widget(sunlight_page)

        return self.sm

if __name__ == '__main__':
    SolarEnergyCalculatorApp().run()
