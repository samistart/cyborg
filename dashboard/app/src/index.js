import React from 'react';
import Plot from 'react-plotly.js';

import ReactDOM from 'react-dom';
import './index.css';

// ========================================
// Test API Fetch
// ========================================

// function myFetch() {
//   const value = fetch('http://127.0.0.1:5000/emails/')
//     .then(function(response) {
//       return response.json();
//     })
//   return value
//   }
// 
// myFetch().then(response => console.log(response.daily_emails.map(i=>i.email_count)))

// ========================================
// Tests Complete
// ========================================

class EmailWidget extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      error: null,
      isLoaded: false,
      items: []
    };
  }

  componentDidMount() {
    fetch("http://localhost:8000/emails/")
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            isLoaded: true,
            daily_emails: result.daily_emails
          });
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          this.setState({
            isLoaded: true,
            error
          });
        }
      )
  }

  render() {
    if (this.state.error) {
      return <div>Error: {this.state.error.message}</div>;
    } else if (!this.state.isLoaded) {
      return <div>Loading...</div>;
    } else {
      return (
        <EmailPlot
          dates={this.state.daily_emails.map(i=>i.date)}
          date_labels={this.state.daily_emails.map(i=>i.pretty_date)}
          email_counts={this.state.daily_emails.map(i=>i.email_count)}
        />
      );
    }
  }  

}

function EmailPlot(props) {
  return(
    <Plot
      data={[
        {type: 'bar', x: props.dates, y: props.email_counts},
      ]}
      layout={
        {
          width: 640,
          height: 480,
          title: 'Email Influx',
          'xaxis': {
            'tickformat': '%y/%m/%d',
            'tickvals': props.dates,
            'ticktext': props.date_labels,
            'tickangle':45
          }
        }
      }
    />
  );
}


// ========================================


class Website extends React.Component {

    render() {

        return (
            <div className="WebSite">
                <p>Hello world</p>
                <EmailWidget/>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Website/>,
    document.getElementById('root')
);
