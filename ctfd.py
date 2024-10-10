import os
import re
import threading
import yaml
import json
from decouple import config
import subprocess
import os.path


# Initialize ctfcli with the CTFD_TOKEN and CTFD_URL.
def init():

    
    CTFD_TOKEN = config("CTFD_TOKEN", default=None)
    CTFD_URL = config("CTFD_URL", default=None)
  
    if not CTFD_TOKEN or not CTFD_URL:
        print("create an .env file with the following fields, CTFD_TOKEN and CTFD_URL")
        exit(1)

    os.system(f"echo '{CTFD_URL}\n{CTFD_TOKEN}\ny' | ctf init")


# Each category is in it's own directory, get the names of all directories that do not begin with '.'.
def get_categories():
    denylist_regex = r'\..*'

    categories = [name for name in os.listdir(".") if os.path.isdir(name) and not re.match(denylist_regex, name)]
    print("Categories: " + ", ".join(categories))
    return categories


# Synchronize all challenges in the given category, where each challenge is in it's own folder.
def sync(category):
    challenges = [f"{category}/{name}" for name in os.listdir(f"./{category}") if os.path.isdir(f"{category}/{name}")]

    for challenge in challenges:
        if os.path.exists(f"{challenge}/challenge.yml"):
            docker_container(challenge)
            print(f"Syncing challenge: {challenge}")
            os.system(f"ctf challenge sync '{challenge}'; ctf challenge install '{challenge}'")


def strip_special_characters(name):
    return (''.join(e for e in name if e.isalnum())).lower()
def docker_container(directory):
    challenge = f"{directory}/challenge.yml"
    if 'challenge.yml' not in challenge:
        return
    chall = open(challenge, 'r')
    challenge_yml = yaml.load(chall, Loader=yaml.FullLoader)
    if 'exposeService' in challenge_yml:
        public_port = challenge_yml['exposeService']['publicPort']
        
        #if we have a docker-compose, we will give the priority to it otherwise we will
        #use the dockerfile
        docker_compose_file = f"{directory}/docker-compose.yml"
        if os.path.exists(docker_compose_file):
            #stop the old docker and spin up the new one
            #this run in deatach mode
            docker_compose_command = f"docker compose -f {docker_compose_file} down --remove-orphans -v && docker-compose -f {docker_compose_file} up --build -d"
            print(docker_compose_command) 
            os.system(docker_compose_command)
        else:
            #building the image based on the docker file
            tag = strip_special_characters(challenge_yml['name'])
            dir = directory.replace(' ', '\\ ') #we need the full path to the dockerfile and need to take care of spacing as well
            os.system(f"docker build -t {tag} {dir}") #build the image tag
            #run the image and start it using the latest build , desired port in deatach mode
            
            internal_port = challenge_yml['exposeService']['internalPort']
            
            #stop the previous image
            os.system(f"docker stop {tag}")
            os.system(f"docker rm {tag}")
            os.system(f"docker run -d --name {tag} -p {public_port}:{internal_port} {tag}:latest")
        
        #we want to update the challenge.yml with the port info
        protocol = challenge_yml['exposeService']['protocol']
        DOMAIN = config("CTFD_DOMAIN", default=None)
        description = challenge_yml['description']
      
        #create the host based on the protocol
        if 'http' in protocol or 'https' in protocol:
            host = f"{protocol}{DOMAIN}:{public_port}"
        elif protocol == 'ssh':
            host = f"{protocol} {DOMAIN} -p {public_port}"
        elif protocol=='nc':
            host = f"{protocol} {DOMAIN} {public_port}"
        
        #removing the old host before appending the new host
        #challenge_yml['description'] = description.replace(host, '') + '\n' + host

        challenge_yml['connection_info']= host
        
        
        #write the new challenge.yml
        chall = open(challenge, 'w')
        yaml.dump(challenge_yml, chall, sort_keys=False)


#dont neeed this yet, might need it once 
# Firewall rules for visible challenges
def firewall(visible, hidden):
    rules = os.popen('gcloud compute firewall-rules --format=json list').read()

    for category in visible:
        for challenge in visible[category]:
            if challenge['port'] and challenge['name'] not in rules:
                os.system(
                    f"""
                        gcloud compute firewall-rules create {challenge['name']} \
                            --allow tcp:{challenge['port']} \
                            --priority 1000 \
                            --target-tags challs
                    """
                )
                print('Created firewall rules for:')
                print(challenge['name'])
    
    for category in hidden:
        for challenge in hidden[category]:
            if challenge['port'] and challenge['name'] in rules:
                os.system(
                    f"""
                        echo -e "Y\n" | gcloud compute firewall-rules delete {challenge['name']}
                    """
                )
                print('Deleted firewall rules for:')
                print(challenge['name'])    


# Synchronize each category in it's own thread.
if __name__ == "__main__":
    init()
    categories = get_categories()

    jobs = []
    for category in categories:
        jobs.append(threading.Thread(target=sync, args=(category, )))
    
    for job in jobs:
        job.start()

    for job in jobs:
        job.join()

    print("Synchronized successfully!")
    print("The following challenges are now visible:")

    """
    for category in visible:
        print(f"\n{category}:")
        print('- ' + '\n- '.join([challenge['name'] for challenge in visible[category]]))

    firewall(visible, hidden)
    print("Firewall rules updated.")
    """