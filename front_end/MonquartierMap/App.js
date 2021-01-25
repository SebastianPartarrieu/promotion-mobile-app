/**
 * Sample React Native App
 * https://github.com/facebook/react-native
 *
 * @format
 * @flow strict-local
 */

import React from 'react';
import {
  SafeAreaView,
  StyleSheet,
  ScrollView,
  View,
  Text,
  StatusBar,
} from 'react-native';

import {
  Header,
  LearnMoreLinks,
  Colors,
  DebugInstructions,
  ReloadInstructions,
} from 'react-native/Libraries/NewAppScreen';

import MapView from 'react-native-maps'

export default function App () 
{    
  return (      
  <MapView   
    style={{flex: 1}}        
    region={{          
      latitude: 42.882004,          
      longitude: 74.582748,          
      latitudeDelta: 0.0922,          
      longitudeDelta: 0.0421        
    }}        
    showsUserLocation={true}      />    
    );  
}
