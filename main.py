from evaluate_user import evaluate_user

def main():
    user_id = ""
    while user_id != 'exit':
        user_id = raw_input("Enter user id: ")
        if user_id != 'exit' and evaluate_user(user_id) == 1:
            print("Cannot evaluate user.\n")

if __name__ == "__main__":
    main()