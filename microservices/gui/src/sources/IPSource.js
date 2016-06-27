import React from 'react';
import $ from 'jquery';
import {ipdiagUrl} from '../config';

class IPSource {
  fetch = (host) => {
    return new Promise((resolve, reject) => {
      $.ajax({
        url: `${ipdiagUrl}${host}`
      })
        .done((data) => {
          if (data.ping_result !== '') {
            resolve(<pre>{data.ping_result}</pre>)
          } else {
            resolve(<pre>{data.ping_error}</pre>);
          }
        })
        .fail((xhr) => {
          if (xhr.responseText) {
            const parsed = JSON.parse(xhr.responseText);
            reject(<pre>{parsed.message}</pre>);
          } else {
            reject(<pre>Could not connect to server!</pre>);
          }
        });
    });
  }
}

export default new IPSource();
