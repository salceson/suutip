/**
 * React Starter Kit (https://www.reactstarterkit.com/)
 *
 * Copyright © 2014-2016 Kriasoft, LLC. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE.txt file in the root directory of this source tree.
 */

import React, {Component, PropTypes} from "react";
import Link from "../Link";

class Navigation extends Component {

  static propTypes = {
    className: PropTypes.string,
  };

  render() {
    return (
      <ul className="nav navbar-nav">
        <li><Link to="/ipdiag">IP Diagnostics Service</Link></li>
        <li><Link to="/users">Users Service</Link></li>
        <li><Link to="/aggregate">Aggregate Service</Link></li>
      </ul>
    );
  }

}

export default Navigation
