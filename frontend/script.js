const apiUrl = "http://127.0.0.1:5000"; // Backend URL


async function fetchTasks() {
    const loadingElement = document.getElementById("loading");
    let timeout;


    try {
        const response = await fetch(`${apiUrl}/tasks`);

        if (!response.ok) {
            throw new Error('Failed to fetch tasks');
        }
        const tasks = await response.json();

        timeout = setTimeout(() => {
            loadingElement.style.display = "block";  
        }, 300); 
        
        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        tasks.forEach(task => {
            const li = document.createElement("li");
            li.textContent = task[1]; 
            if (task[2] === 1) li.classList.add("completed");

            const completeBtn = document.createElement("button");
            completeBtn.textContent = "Complete";
            completeBtn.onclick = () => completeTask(task[0]);

            const deleteBtn = document.createElement("button");
            deleteBtn.textContent = "Delete";
            deleteBtn.onclick = () => deleteTask(task[0]);

            li.appendChild(completeBtn);
            li.appendChild(deleteBtn);
            taskList.appendChild(li);


        });
    } catch (error) {
        console.error('Error fetching tasks:', error);
    }finally {
        clearTimeout(timeout);  
        loadingElement.style.display = "none";
    }
    
}

// Add task
async function addTask() {
    const taskInput = document.getElementById("taskInput").value;
    if (!taskInput) return;

    await fetch(`${apiUrl}/add`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ task_name: taskInput })
    });

    document.getElementById("taskInput").value = "";
    fetchTasks();
}

// Complete task
async function completeTask(id) {
    await fetch(`${apiUrl}/update/${id}`, { method: "PUT" });
    fetchTasks();
}

// Delete task
async function deleteTask(id) {
    await fetch(`${apiUrl}/delete/${id}`, { method: "DELETE" });
    fetchTasks();
}

// Load tasks on page load
window.onload = fetchTasks;
