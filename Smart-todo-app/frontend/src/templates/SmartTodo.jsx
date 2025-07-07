import React, { useEffect, useState } from 'react';
import axios from 'axios';
import '../index.css';

export default function SmartTodoStyled() {
  const [tasks, setTasks] = useState([]);
  const [categories, setCategories] = useState([]);

  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState(1);
  const [deadline, setDeadline] = useState('');
  const [status, setStatus] = useState(false);
  const [categoryId, setCategoryId] = useState('');

  // const [suggestion, setSuggestion] = useState('');
  const [darkMode, setDarkMode] = useState(false);

  const [contextText, setContextText] = useState('');
  const [insights, setInsights] = useState('');
  const [suggestedTask, setSuggestedTask] = useState('');
  const [loading, setLoading] = useState(false);

  // Fetch tasks
  const fetchTasks = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/tasks/');
      setTasks(res.data);
    } catch (error) {
      console.error("Error fetching tasks:", error);
    }
  };

  // Fetch categories
  const fetchCategories = async () => {
    try {
      const res = await axios.get('http://localhost:8000/api/categories/');
      setCategories(res.data);
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  };

  // Create task
  const createTask = async () => {
    try {
      await axios.post('http://localhost:8000/api/tasks/create/', {
        title,
        description,
        priority,
        deadline,
        is_completed: status,
        category_id: categoryId,
      });

      setTitle('');
      setDescription('');
      setPriority(1);
      setDeadline('');
      setStatus(false);
      setCategoryId('');
      fetchTasks();
    } catch (error) {
      console.error("Error creating task:", error.response?.data || error.message);
    }
  };

  // AI Suggestions
  const handleSuggestion = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/context/suggest/', {
        
          text: "Busy fixing bugs, client call at 6 PM"
      });
      setSuggestedTask(response.data.task_suggestion);
    } catch (error) {
      setSuggestedTask(`Error: ${error.response?.data?.error || "Something went wrong"}`);
    }
    setLoading(false);
  };

  // Submit AI context
  const handleInsight = async () => {
    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/context/insight/', {
        text: contextText,
      });
      setInsights(response.data.insights);
    } catch (error) {
      setInsights(`Error: ${error.response?.data?.error || "Something went wrong"}`);
    }
    setLoading(false);
  };
  
  const toggleTheme = () => setDarkMode(prev => !prev);

  useEffect(() => {
    fetchTasks();
    fetchCategories();
  }, []);

  return (
    <div className={`container ${darkMode ? 'dark' : ''}`}>
      <h1 className="title"> Smart Todo App</h1>

      <div className="input-group grid gap-4 mb-6">
        <input
          value={title}
          onChange={e => setTitle(e.target.value)}
          placeholder="Task title..."
          className="input"
        />

        <textarea
          value={description}
          onChange={e => setDescription(e.target.value)}
          placeholder="Description"
          className="input"
        />

        <select
          value={categoryId}
          onChange={e => setCategoryId(e.target.value)}
          className="input"
        >
          <option value="">Select Category</option>
          {categories.map(cat => (
            <option key={cat.id} value={cat.id}>{cat.name}</option>
          ))}
        </select>

        <input
          type="number"
          value={priority}
          onChange={e => setPriority(parseInt(e.target.value))}
          placeholder="Priority (1-5)"
          min={1}
          max={5}
          className="input"
        />

        <label htmlFor="Deadline">Set the deadline</label>
        <input
          type="datetime-local"
          value={deadline}
          onChange={e => setDeadline(e.target.value)}
          className="input"
        />

        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={status}
            onChange={e => setStatus(e.target.checked)}
          />
          <span>Status: Completed</span>
        </label>

        <div className="flex gap-2">
          <button onClick={createTask} className="add-button">Add</button>
          <button  onClick={handleSuggestion}disabled={loading} className="suggest-button">{loading ? 'Suggesting...' : 'Suggest Task'}</button>
        </div>
      </div>

      {suggestedTask && (
        <p className="suggestion"><strong>AI:</strong> {suggestedTask}</p>
      )}

      <div className="context-entry-section p-4 border rounded-md mb-6">
        <h2 className="text-lg font-semibold mb-2">Context Entry (AI Insight)</h2>
        <textarea
          value={contextText}
          onChange={(e) => setContextText(e.target.value)}
          placeholder="Describe your schedule or task-related context..."
          className="input"
        />
        <button
           onClick={handleInsight}
          disabled={loading}
          className="add-button"
        >
         {loading ? 'Generating Insights...' : 'Get Insights'}
        </button>

        {insights  && (
          <p className="mt-4 text-sm text-blue-800 bg-blue-100 p-2 rounded">
            <strong>AI Insight: {insights}</strong>
          </p>
        )}
      </div>

      <div className="task-list">
        {tasks.map(task => (
          <div key={task.id} className="task-item p-4 border rounded-lg shadow-md mb-4">
            <h2 className="text-xl font-semibold mb-2">{task.title}</h2>
            <p className="text-gray-700 mb-1"><strong>Description:</strong> {task.description}</p>
            <p className="text-gray-700 mb-1"><strong>Category:</strong> {task.category?.name || 'Uncategorized'}</p>
            <p className="text-gray-700 mb-1"><strong>Priority Score:</strong> {task.priority}</p>
            <p className="text-gray-700 mb-1"><strong>Deadline:</strong> {new Date(task.deadline).toLocaleString()}</p>
            <p className="text-gray-700 mb-1"><strong>Status:</strong> {task.is_completed ? "Completed" : "Pending"}</p>
            <p className="text-sm text-gray-500">
              Created: {new Date(task.created_at).toLocaleString()} | Updated: {new Date(task.updated_at).toLocaleString()}
            </p>
          </div>
        ))}
      </div>

      <div style={{ textAlign: 'center' }}>
        <button onClick={toggleTheme} className="theme-toggle">
          Toggle {darkMode ? 'Light' : 'Dark'} Mode
        </button>
      </div>
    </div>
  );
}