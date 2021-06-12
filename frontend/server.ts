import 'zone.js/dist/zone-node';
import {enableProdMode} from '@angular/core';
// Express Engine
import {ngExpressEngine} from '@nguniversal/express-engine';
// Import module map for lazy loading
import {provideModuleMap} from '@nguniversal/module-map-ngfactory-loader';

import * as express from 'express';
import {join} from 'path';
import {createDocument,createDOMImplementation,createWindow} from 'domino';
/*import {createDocument,createWindow} from 'domino';*/

// Faster server renders w/ Prod mode (dev mode never needed)
enableProdMode();

// Express server
export const app = express();
const compression = require('compression');
var cookieParser = require('cookie-parser')

const PORT = process.env.PORT || 82;
var appRoot = process.env.PWD;
/*const DIST_FOLDER = process.cwd();*/
const DIST_FOLDER = join(process.cwd(), 'dist/browser');

const domino = require("domino");
const fs = require("fs");
const path = require("path");
const templateA = fs
  .readFileSync(path.join("dist/browser", "index.html"))
  .toString();
const win = domino.createWindow(templateA);
win.Object = Object;
win.Math = Math;
console.log(appRoot);
global["window"] = win;
Object.defineProperty(win.document.body.style, 'transform', {
  value: () => {
    return {
      enumerable: true,
      configurable: true
    };
  },
});

global["document"] = win.document;
global['CSS'] = null;
global['File'] = null;
global["branch"] = null;
global["object"] = win.object;
global['HTMLElement'] = win.HTMLElement;
global['navigator'] = win.navigator;
global['localStorage'] = win.localStorage;
global['Event'] = win.Event;
global['MouseEvent'] = win.MouseEvent;
global['KeyboardEvent'] = win.Event;

// * NOTE :: leave this as require() since this file is built Dynamically from webpack
const {AppServerModuleNgFactory, LAZY_MODULE_MAP} = require('./dist/server/main');


// Our Universal express-engine (found @ https://github.com/angular/universal/tree/master/modules/express-engine)
app.use(compression());
app.use(cookieParser())

app.engine('html', ngExpressEngine({
  bootstrap: AppServerModuleNgFactory,
  providers: [
    provideModuleMap(LAZY_MODULE_MAP)
  ]
}));

app.set('view engine', 'html');
app.set('views', DIST_FOLDER);

// Example Express Rest API endpoints
// app.get('/api/**', (req, res) => { });
// Serve static files from /browser
app.get('*.*', express.static(DIST_FOLDER, {
  maxAge: '1y'
}));

// All regular routes use the Universal engine
/*app.get('*', (req, res) => {
  res.render('index', { req });
});*/
app.get('/api/*',(req,res) => {
  res.status(404).send('');

});

app.get('/apple-app-site-association', function (req, res) {
   console.log(req + "&&&&&&&&&&&&&&&&77")
  // console.log("fs ="+fs)
  // console.log("path ="+path)
  console.log(appRoot)
  var options = {
  headers: {
  'X-Content-Type-Options': 'nosniff',
  'Content-Type': 'application/json'
  }
  }
  res.sendFile('/home/lifco/frontend/apple-app-site-association', options, function (err) {
  if (err) {
  console.log(err)
  console.log(__dirname)
  } else {
  res.status(200)
  res.end()
  }
  })
  })

app.get('*', (req, res) => {
  res.render('index', {
    req: req,
    res: res,
    providers: [
      {
        provide: 'REQUEST', useValue: (req)
      },
      {
        provide: 'RESPONSE', useValue: (res)
      },
       // { 
       //   provide: ERROR_WRAPPER, useValue: (errorWrapper)
       // },
    ]
  },
  
/*  (err, html) => {
            if (err) {
                Log.error("NG render error", err);
                throw err;
            }
            if(errorWrapper.error)
            {
                //handle your error here
            }
            res.send(html);
        }*/
  );
});
