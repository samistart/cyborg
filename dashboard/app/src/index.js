import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';


class Website extends React.Component {

    render() {

        return (
            <div className="WebSite">
                <p>Hello world</p>
            </div>
        );
    }
}

// ========================================

ReactDOM.render(
    <Website/>,
    document.getElementById('root')
);
