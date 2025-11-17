from inputevents import load_inputevents_cv_dict


def main() :
    data = load_inputevents_cv_dict()
    print (data[0])

if __name__ == "__main__":
    main()