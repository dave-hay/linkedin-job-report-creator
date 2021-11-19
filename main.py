from creator import PullJob

# For Test name
url = input('Enter URL')
file = input('job')
nouns = 10
verbs = 10

pull = PullJob(url, file, nouns, verbs)

if __name__ == '__main__':
    pull.run_all()
