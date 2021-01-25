
import React from "react";
import {MapView, Marker} from 'react-native-maps';
import PropTypes from 'prop-types';
import csvjson from "../constants/csvjson";

class Map extends React.Component {
    render(){
         return (         
            <MapView   
             style={{flex: 1}}        
             region={{         
                    latitude: 48.856614,          
                    longitude: 2.3522219,          
                    latitudeDelta: 1,          
                    longitudeDelta: 1        
                  
                 }}       
            //showsUserLocation={true}
            //followsUserLocation={true}
        
            >
                <Marker
                    coordinate={{         
                    latitude: 48.856614,          
                    longitude: 2.3522219}}
                    title={"qbsfmvjgef"}
                    description={"qjzvbiu"}
                >
                </Marker>
            </MapView>
    );  
}
}


export default Map;