import React from 'react';
import $ from 'jquery';
import {aggregateUrl} from '../config';

class AggregateSource {
  search = (name) => {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: `${aggregateUrl}${name}`
      })
        .done((data) => {
          if (data.users !== undefined) {
            resolve(data.users)
          } else {
            reject('Failed to fetch users from database!');
          }
        })
        .fail((xhr) => {
          reject('Could not connect to server!')
        });
    });
  };
}

export default new AggregateSource();
