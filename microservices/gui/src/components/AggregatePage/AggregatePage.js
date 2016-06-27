import React, {Component, PropTypes} from 'react';
import withStyles from 'isomorphic-style-loader/lib/withStyles';
import s from './AggregatePage.scss';
import AggregateSearchUsers from './AggregateSearchUsers';

class AggregatePage extends Component {

  static contextTypes = {
    onSetTitle: PropTypes.func.isRequired
  };

  render() {
    const title = 'Aggregate service';
    this.context.onSetTitle(title);

    return (
      <div className={s.root}>
        <div className={s.container}>
          <h2>{title}</h2>
          <h3>Search and ping users</h3>
          <AggregateSearchUsers/>
        </div>
      </div>
    );
  }

}

export default withStyles(AggregatePage, s);
