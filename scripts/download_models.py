import argparse
from huggingface_hub import hf_hub_download
from os.path import isfile

def parse_lines(lines,force=False,local_dir=False):
   
   if not local_dir:
    local_dir = "./models"

    for line in lines:
        # print(f'>{line}')
        line = line.lstrip()
        
        if line.startswith("#"):
            print("comment skipped..")
            continue

        repo_id, file = line.split(":",2)
        
        if not force and isfile(f"{local_dir}/{file}"):    
            print(f"{file} already exists - skipping..")
            continue
        
        print(f"downloading model {repo_id}:{file}..")

        hf_hub_download(repo_id=repo_id, 
                        filename=file, 
                        local_dir=local_dir,
                        #force_download=force,
                        local_dir_use_symlinks=False)
    
def main():
    parser = argparse.ArgumentParser(description='Download and Install models from huggingface')

    parser.add_argument('-f', '--file'   , help='file with model urls', default='./models.txt')
    parser.add_argument('-v', '--verbose', action='store_true') 
    parser.add_argument('--force', action='store_true', default=False, help ='re-download models') 

    args = parser.parse_args()

    if not args.file:
        print('Error: missing --file')
        parser.print_help()
        return -1
    
    print(f'Processing {args.file}')

    try:
        with open(args.file) as f:
            lines = [line.rstrip() for line in f]
            parse_lines(lines,args.force)

    except FileNotFoundError as e:
        print(f'FileNotFoundError: {str(e)}')
    
# hf_hub_download(repo_id="eachadea/ggml-vicuna-13b-4bit", filename="ggml-vicuna-13b-4bit.bin", local_dir="./models")

main()