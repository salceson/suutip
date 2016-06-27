import React, {Component} from 'react';
import Link from '../Link';
import Navigation from '../Navigation';

class Header extends Component {

  render() {
    return (
      <nav className="navbar navbar-inverse navbar-fixed-top">
        <div className="container">
          <div className="navbar-header">
            <button type="button" className="navbar-toggle collapsed" data-toggle="collapse"
                    data-target="#navbar" aria-expanded="false" aria-controls="navbar">
              <span className="sr-only">Toggle navigation</span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
              <span className="icon-bar"></span>
            </button>
            <Link to="/" className="navbar-brand">GUI Microservice</Link>
          </div>
          <div id="navbar" className="navbar-collapse collapse">
            <Navigation/>
          </div>
        </div>
      </nav>
    );
  }

}

export default Header;
