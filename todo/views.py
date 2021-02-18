from django.shortcuts import redirect, render
from django.http import Http404
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def index_view(request):
    #mengambil semua data task
    tasks = Task.objects.all()
    context = {
            'tasks': tasks
            }
    #memparsing data task ke template
    return render(request, 'todo/index.html', context)

def detail_view(request, task_id):
    #mengambil data task berdasarkan task ID
    try:
        task = Task.objects.get(pk=task_id)
        context = {
                'task': task
        }
    except Task.DoesNotExist:
        raise Http404("Task tidak ditemukan")
    return render(request, 'todo/detail.html', context)

def create_view(request):
    #cek method pada request
    if request.method == 'POST':
        #membuat objek dari class TaskForm
        new_task = TaskForm(request.POST)
        #cek validasi form
        if new_task.is_valid():
            #simpan ke dalam table tasks
            new_task.save()
            #mengeset pesan sukses dan redirect ke halaman daftar task
            messages.success(request, 'Sukses menambah Task baru')
            return redirect('todo:index')
    #jika method bukan POST
    else:
        #membuat objek dari class TaskForm
        form = TaskForm()
    return render(request, 'todo/form.html', {'form': form})

def update_view(request, task_id):
    try:
        #mengambil data task yang akan diubah berdasarkan task id
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        #jika task tisak ditemukan
        raise Http404("Task tidak ditemukan")
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            #simpan perubahan data
            form.save()
            #,engeset pesan Sukses
            messages.success(request, 'Sukses mengubah Task')
            return redirect('todo:index')
            #jika method nya bukan POST
    else:
        #buat object dari class TaskForm
        form = TaskForm(instance=task)
        #merender template form dengan memparsin data form
    return render(request, 'todo/form.html', {'form': form})

def delete_view(request, task_id):
    try:
        #mengambil data task yang akan dihapus
        task = Task.objects.get(pk=task_id)
        #menghapus data dari table tasks
        task.delete()
        #mengeset pesan sukses
        messages.success(request, 'Sukses menghapus Task')
        return redirect('todo:index')
    except Task.DoesNotExist:
        raise Http404("Task tidak ditemukan")
