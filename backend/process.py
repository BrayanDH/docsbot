import re
import chromadb
from chromadb.config import Settings
import os
document_id = 1


db_path = "./db"

def process_info(texto, database, titulo, filename, document_id):
    with chromadb.PersistentClient(path=db_path) as chroma_client:
        if not chroma_client.collection_exists(name=database):
            collection = chroma_client.create_collection(name=database)
        else:
            collection = chroma_client.get_collection(name=database)

        generate_embeddings(texto, titulo, filename, collection, document_id)

    return True


def read_processed_files(log_file_path):
    
    if not os.path.exists(log_file_path):
        return []
    
    with open(log_file_path, 'r') as f:
        processed = [line.strip() for line in f]
    
    return processed

def process_files(documents):

    # crear la base de datos si no existe
  if os.path.exists(os.path.join(db_path, "chroma.sqlite3")):
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name="test_collection_one")
    
  else:
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.create_collection(name="test_collection_one")

  # leer el archivo de texto con los archivos ya procesados
  log_file_path = 'processed_files.txt'
  processed = read_processed_files(log_file_path)


  for file in documents:
    
    if file.filename not in processed:
      print("processing file: " + file.filename)
      markdown_text = file.read().decode()
      chunks = split_text(markdown_text)
      document_title = get_title(markdown_text)
      generate_embeddings(chunks, document_title, file.filename, collection)


      # guardar el nombre del archivo en el archivo de texto
      with open(log_file_path, 'a') as f:
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


def consulta(query):
    print("mi consulta:::: "+query)
    chroma_client = chromadb.PersistentClient(path=db_path)
    collection = chroma_client.get_collection(name="posfile_test")
    results = collection.query(
        query_texts=[query],
        n_results=2,
    )
    chroma_client.stop()  # Cierra la conexión después de usarla
    return results