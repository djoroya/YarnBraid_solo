from concurrent.futures import ThreadPoolExecutor, as_completed
import multiprocessing
from IPython.display import display, HTML, clear_output

def mostrar_barra_de_progreso_html(tareas_completadas, total_tareas):
    porcentaje_completado = (tareas_completadas / total_tareas) * 100
    barra_html = f"""
    <div style="border: 1px solid black; width: 500px">
        <div style="background-color: #4CAF50; width: {porcentaje_completado}%; height: 20px"></div>
    </div>
    <p>{tareas_completadas} de {total_tareas} tareas completadas ({porcentaje_completado:.2f}% completado).</p>
    """
    clear_output(wait=True)
    display(HTML(barra_html))
    
def parallel(tareas, max_tareas_simultaneas):
    num_cpus = multiprocessing.cpu_count()
    max_tareas_simultaneas = min(max_tareas_simultaneas, num_cpus)
    
    tareas_completadas = 0
    total_tareas = len(tareas)

    results = dict()
        
    names = [str(i) for i in range(len(tareas))]
    for tarea,name in zip(tareas,names):
        tarea.__annotations__ = {"name": name}

    if len(names) != len(set(names)):
        raise ValueError('Hay tareas repetidas.')

    with ThreadPoolExecutor(max_workers=max_tareas_simultaneas) as executor:
        future_to_task = {executor.submit(tarea): tarea for tarea in tareas}
        
        for future in as_completed(future_to_task):
            tarea = future_to_task[future]
            try:
                result = future.result()
                results[tarea.__annotations__["name"]] = result
            except Exception as exc:
                print(f'La tarea {tarea.__name__} generó una excepción: {exc}')
            tareas_completadas += 1
            mostrar_barra_de_progreso_html(tareas_completadas, total_tareas)

    # sort results by key
    results = {k: results[k] for k in sorted(results)}
    # convert to list and remove keys
    results = list(results.values())
    return results