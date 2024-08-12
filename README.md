# T2 Parser - A high performance POS parser

### Step 1: Create virtual env using conda
conda create --prefix ./t2parser_env python=3.11
### Step 2: Activate conda virtual env
conda activate ./2parser_env
### Step 3: Install requirements
pip install -r requirements.txt
### Step optional: Install all package for data analysis with anaconda
conda install anaconda
### Notes: Deactivate virtual env
conda deactivate
### Create .env file with:
PROJECT_NAME=T2 PARSER  
DATABASE_URL=sqlite:///./data_dir/t2parser.db  
DATA_DIR='./data_dir'  