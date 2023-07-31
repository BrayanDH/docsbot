import re
import chromadb
from chromadb.config import Settings
import os
document_id = 1

db_path = os.path.join(os.path.dirname(__file__), "local_db")

def process_files(documents):
  
    # crear la base de datos si no existe
  if not os.path.exists(db_path):
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.create_collection(name="test_collection_one")
  else:
     chroma_client = chromadb.PersistentClient(path=db_path)
     collection = chroma_client.get_collection(name="test_collection_one")

  # crear el archivo de log si no existe
  processed_files = 'processed_files.txt'
  if not os.path.exists(processed_files):
    file = open(processed_files, 'a')

  # # Leer los archivos ya procesados
  with open(processed_files) as f:
    processed = [line.strip() for line in f.readlines()]


  for file in documents:
    
    if file.filename not in processed:
      print("processing file: " + file.filename)
      markdown_text = file.read().decode()
      chunks = split_text(markdown_text)
      document_title = get_title(markdown_text)
      generate_embeddings(chunks, document_title, file.filename, collection)


      # guardar el nombre del archivo en el archivo de texto
      with open(processed_files, 'a') as f:
        f.write(file.filename + '\n')
        f.close()
        print(f"{file.filename} writted...")
    else:
        print(f"{file.filename} already processed...")
        continue

  chroma_client.stop()
  return True



def generate_embeddings(chunks, document_title, file_name, collection):
    global document_id
    for chunk in chunks:
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        document_id = document_id + 1


def get_title(file):
    match = re.search(r"title:\s+(.+)\s+", file)
    if match:
        title = match.group(1)
        return title
    else:
        " "


def split_text(file):
    separator = "\n### "
    return file.split(separator)


def query_collection(query):
    chroma_client = chromadb.PersistentClient(path='local_db')
    collection = chroma_client.get_collection(name="test_collection_one")
    results = collection.query(
        query_texts=[query],
        n_results=2,
    )
    chroma_client.stop()  # Cierra la conexión después de usarla
    return results


