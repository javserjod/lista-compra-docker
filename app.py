import streamlit as st      # framework apps web interactivas
import redis                # BBDD

# configuración de la página
st.set_page_config(page_title="Lista de la Compra", page_icon="🛒")
st.title("🛒 Lista de la Compra")

# conexión a Redis (imagen de Docker Hub)
# 'redis_db' es el nombre del servicio de datos definido en el archivo YAML
db = redis.Redis(host='redis_db', port=6379, decode_responses=True)

# --- SECCIÓN AÑADIR PRODUCTOS ---
nuevo_item = st.text_input("¿Qué necesitas comprar?",
                           placeholder="Ej: Leche, Huevos...")

if st.button("Añadir a la lista"):
    if nuevo_item:
        # guardamos nuevo elemento en un set de Redis (no habrá duplicados)
        db.sadd("lista_compra", nuevo_item)
        st.rerun()

# --- SECCIÓN MOSTRAR LISTA ---
st.subheader("Pendiente de comprar:")
items = db.smembers("lista_compra")

if items:        # si hay elementos en la lista de la compra, mostrarlos:
    for item in sorted(items):
        col1, col2 = st.columns([0.8, 0.2])
        col1.write(f"🔹 {item}")

        # botón para eliminar elemento de la lista de la compra
        if col2.button("✅", key=item):
            db.srem("lista_compra", item)
            st.rerun()
else:
    st.info("La lista está vacía. ¡Buen trabajo!")

# --- SECCIÓN BOTÓN DE LIMPIEZA ---
if items:
    if st.button("Borrar toda la lista"):
        db.delete("lista_compra")     # borrar lista de la compra por completo
        st.rerun()
