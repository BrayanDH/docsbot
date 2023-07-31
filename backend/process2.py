import re
import chromadb
from chromadb.config import Settings

# settings es una clase de la biblioteca chromadb que nos permite configurar la conexión a la base de datos
settings = Settings()

# document_id es una variable que utilizaremos para almacenar el ID del documento que estamos procesando
document_id = 1

def process_files(documents):
    # chroma_client es una clase de la biblioteca chromadb que nos permite interactuar con la base de datos
    chroma_client = chromadb.PersistentClient(path='local_db')
    
    # create_collection crea una nueva colección en la base de datos con el nombre que le pasamos
    collection = chroma_client.create_collection(name="test_collection_one")
    
    # Iteramos sobre los documentos que se pasan como parámetro en la función process_files
    for file in documents:
        # Esteprint() imprime en la pantalla el nombre del archivo que estamos procesando
        print("processing file: " + file.filename)

        
        # markdown_text es una variable que contiene el texto del archivo en formato markdown
        markdown_text = file.read().decode()
        
        # chunks es una lista que contiene los fragmentos de texto (chunks) que se han dividido del texto original
        chunks = split_text(markdown_text)
        
        # document_title es una variable que contiene el título del documento
        document_title = get_title(markdown_text)
        
        # Generamos los embeddings para cada fragmento de texto (chunk) y los agregamos a la colección
        generate_embeddings(chunks, document_title, file.filename, collection)
    
    # chroma_client.stop() es una función que cierra la conexión a la base de datos después de utilizarla
    chroma_client.stop()

def generate_embeddings(chunks, document_title, file_name, collection):
    # Iteramos sobre los fragmentos de texto (chunks) y generamos un embedding para cada uno
    for chunk in chunks:
        # collection.add() agrega un nuevo documento a la colección con los metadatos especificados
        collection.add(
            metadatas={
                "document_title": document_title if document_title is not None else "",
                "file_name": file_name
            },
            documents=chunk,
            ids=[str(document_id)]
        )
        # document_id se incrementa para cada documento que agregamos a la colección
        document_id = document_id + 1

def get_title(file):
    # Utilizamos la función re.search() para buscar el título del archivo en el texto
    match = re.search(r"title:\s+(.+)\s+", file)
    
    # Si encontramos un título, lo extraemos y lo devolvemos
    if match:
        title = match.group(1)
        return title
    else:
        # Si no encontramos título, devolvemos un espacio en blanco
        return ""

def split_text(file):
    # Definimos el separador que utilizaremos para dividir el archivo de texto en varias partes
    separator = "\n### "

    # Utilizamos el método split() para dividir el archivo de texto en una lista de cadenas
    # El método split() toma dos argumentos: el separador y el número de partes que queremos dividir el archivo en
    return file.split(separator)

def query_collection(query):
    # Creamos una instancia de la clase PersistentClient de chromadb para conectarnos a la base de datos
    chroma_client = chromadb.PersistentClient(path='local_db')

    # Obtener la colección de la base de datos con el nombre especificado
    collection = chroma_client.get_collection(name="test_collection_one")

    # Realizamos una consulta en la colección utilizando el método query() y pasamos como argumento la cadena de texto de la consulta
    # El método query() devuelve un conjunto de resultados
    results = collection.query(query_texts=[query], n_results=2)

    # Cerramos la conexión con la base de datos después de utilizarla
    chroma_client.stop()

    # Devolvemos los resultados de la consulta
    return results