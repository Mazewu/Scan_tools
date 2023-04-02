import re
class spider():
    def run(self, url, html,result_queue):
        pattern = re.compile(r'([\w-]+@[\w-]+\.[\w-]+)+')
        email_list = re.findall(pattern, html)
        if email_list:
            for email in email_list:
                result_queue.put(("email:"+ email))
                print(email)
            return True
        return False
