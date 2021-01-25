
import React from "react";
import {MapView, Marker} from 'react-native-maps';
import csvjson from "../constants/csvjson";

function MakeMap(item = csvjson[0]) 
{
         return (        
            <MapView   
             style={{flex: 1}}        
             region={{         
                    latitude: item.coordinates.latitude,          
                    longitude: item.coordinates.longitude,          
                    latitudeDelta: 1,          
                    longitudeDelta: 1        
                  
                 }}       
            //showsUserLocation={true}
            //followsUserLocation={true}
        
            >
                <Marker
                    coordinate={{         
                    latitude: item.coordinates.latitude,          
                    longitude: item.coordinates.latitude}}
                    title={item.nom}
                    description={item.description}
                >
                </Marker>
            </MapView>
    );  
    }


export default MakeMap;