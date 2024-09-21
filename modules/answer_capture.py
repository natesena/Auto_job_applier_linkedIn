from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from modules.clickers_and_finders import try_xp

def capture_final_answers(driver):
    final_questions_list = []
    all_questions = driver.find_elements(By.CLASS_NAME, "jobs-easy-apply-form-element")

    for Question in all_questions:
        label_element = try_xp(Question, ".//label", False)
        label = label_element.text if label_element else "Unknown"
        
        select = try_xp(Question, ".//select", False)
        if select:
            answer = Select(select).first_selected_option.text
            final_questions_list.append((label, answer, "select"))
            continue

        radio = try_xp(Question, './/input[@type="radio"]:checked', False)
        if radio:
            answer = radio.find_element(By.XPATH, './following-sibling::label').text
            final_questions_list.append((label, answer, "radio"))
            continue

        text = try_xp(Question, ".//input[@type='text']", False)
        if text:
            answer = text.get_attribute("value")
            final_questions_list.append((label, answer, "text"))
            continue

        textarea = try_xp(Question, ".//textarea", False)
        if textarea:
            answer = textarea.get_attribute("value")
            final_questions_list.append((label, answer, "textarea"))
            continue

        checkbox = try_xp(Question, ".//input[@type='checkbox']", False)
        if checkbox:
            answer = "Checked" if checkbox.is_selected() else "Unchecked"
            final_questions_list.append((label, answer, "checkbox"))
            continue

    return final_questions_list
