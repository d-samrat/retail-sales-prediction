import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import './App.css';

function App() {
  const [category, setCategory] = useState('');
  const [selectedDate, setSelectedDate] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setPrediction(null);

    if (!selectedDate || !category) {
      setError('Please select both a category and a date.');
      return;
    }

    const requestData = {
      category: category,
      date: selectedDate.toLocaleDateString('en-CA'), // returns yyyy-mm-dd in local time
    };

    try {
      const response = await axios.post('http://127.0.0.1:8000/predict_sales/', requestData);
      setPrediction(response.data.predicted_sales);
    } catch (error) {
      if (error.response) {
        setError(error.response.data.detail);
      } else {
        setError('Server not responding');
      }
    }
    
  };
  
  const fakeFutureDate = (date) => {
  const fakeDate = new Date(date);
  fakeDate.setFullYear(fakeDate.getFullYear() + 1);
  return fakeDate.toLocaleDateString('en-CA'); // returns YYYY-MM-DD in local time
};

  const modalRef = useRef();

  const handleOverlayClick = (e) => {
    if (modalRef.current && !modalRef.current.contains(e.target)) {
      setPrediction(null); // close modal
    }
  };


  return (
    <div className="App">
      <h1>Retail Sales <br />Prediction</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Select Category:</label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            required
          >
            <option value="">-- Select Category --</option>
            <option value="Electronics">Electronics</option>
            <option value="Beauty">Beauty</option>
            <option value="Clothing">Clothing</option>
          </select>
        </div>
        <div>
          <label>Select Date:</label>
          <div style={{ width: '100%' }}>
  <DatePicker
  selected={
    selectedDate
      ? new Date(new Date(selectedDate).setFullYear(selectedDate.getFullYear() + 1))
      : null
  }
  onChange={(displayedDate) => {
    const trueDate = new Date(displayedDate);
    trueDate.setFullYear(trueDate.getFullYear() - 1); // back to 2023
    setSelectedDate(trueDate);
  }}
  dateFormat="yyyy-MM-dd"
  placeholderText="Click to select a date"
  minDate={new Date('2024-01-01')}
  maxDate={new Date('2024-12-31')}
  showMonthDropdown
  showYearDropdown
  dropdownMode="select"
/>
  {selectedDate && (
    <button
      type="button"
      onClick={() => setSelectedDate(null)}
      className="clear-date-btn"
    >
       ✕
    </button>
  )}
</div>
        </div>
        <button type="submit">Predict</button>
      </form>

      {/* {prediction !== null && selectedDate && (
        // <div>
        //   <h2>
        //     📊 The predicted number of sales of <strong>{category}</strong> on <strong>{selectedDate.toISOString().split('T')[0]}</strong>: <strong>{prediction.toFixed(2)}</strong> units
        //   </h2>
        // </div>
      )} */}

      {error && (
        <div style={{ color: 'red' }}>
          <p>⚠️ {error}</p>
        </div>
      )}
      <div className='Tagline'>
          Forecast Tomorrow's Sales, Today.
      </div>
      <div className="video-background">
        <video autoPlay loop muted playsInline>
        <source src="/bg.mp4" type="video/mp4" />
    Your browser does not support the video tag.
        </video>
    </div>
    {prediction !== null && selectedDate && (
  <div className="overlay" onClick={handleOverlayClick}>
    <div className="modal" ref={modalRef}>
      <h2>
        <strong>{prediction.toFixed(2)} units</strong><br />of<br />
        <strong>{category}</strong><br />will be sold<br />on<br />
        <strong>{fakeFutureDate(selectedDate)}</strong>
      </h2>
      <button onClick={() => setPrediction(null)}>Close</button>
    </div>
  </div>
)}



    </div>
  );
}

export default App;
