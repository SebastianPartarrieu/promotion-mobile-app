import React, { Component } from "react";
import {
  StyleSheet,
  Dimensions,
  ScrollView,
  Image,
  ImageBackground,
  Platform,
  View
} from "react-native";
import { Block, Text, theme } from "galio-framework";
import { Button, ProfileCard } from "../components";
import { Images, argonTheme} from "../constants";
import { HeaderHeight } from "../constants/utils";
import PropTypes from 'prop-types';
import articles from "../constants/articles"






const { width, height } = Dimensions.get("screen");

const thumbMeasure = (width - 48 - 32) / 3;

//const {item} = articles

//console.log(articles[1])

item = articles[1]

function Profile(id) {
  //id = {props}
  console.log(id)
  //item = articles[id]

  return (
    <Block flex style={styles.profile}>
      <Block flex>
        <ImageBackground
          source={Images.ProfileBackground}
          style={styles.profileContainer}
          imageStyle={styles.profileBackground}
        >
          <ScrollView
            showsVerticalScrollIndicator={false}
            style={{ width, marginTop: '25%' }}
          >
            <Block flex style={styles.profileCard}>
              <Block middle style={styles.avatarContainer}>
                <Image
                  source={{ uri: item.image }}
                  style={styles.avatar}
                />
              </Block>
              <Block style={styles.info}>
                <Block
                  middle
                  row
                  space="evenly"
                  style={{ marginTop: 10, paddingBottom: 0}}
                >
                  <Button
                    small
                    style={{ backgroundColor: argonTheme.COLORS.INFO }}
                  >
                    SITE WEB
                  </Button>
                </Block>
                
              </Block>
              <Block flex>
                <Block middle style={styles.nameInfo}>
                  <Text bold size={28} color="#32325D">
                    {item.nom}
                  </Text>
                  <Text size={16} color="#32325D" style={{ marginTop: 0 }}>
                    {item.adresse}
                  </Text>
                </Block>
                <Block middle style={{ marginTop: 20, marginBottom: 16 }}>
                  <Block style={styles.divider} />
                </Block>
                <Block middle>
                  <Text
                    size={16}
                    color="#525F7F"
                    style={{ textAlign: "center" }}
                  >
                    {item.description}
                  </Text>
                  <Button
                    color="transparent"
                    textStyle={{
                      color: "#233DD2",
                      fontWeight: "500",
                      fontSize: 16
                    }}
                  >
                    Show more
                  </Button>
                </Block>
                <Block
                  row
                  space="between"
                >
                  <Text bold size={16} color="#525F7F" style={{marginTop: 12}}>
                    Album
                  </Text>
                  <Button
                    small
                    color="transparent"
                    textStyle={{ color: "#5E72E4", fontSize: 12, marginLeft: 24 }}
                  >
                    View all
                  </Button>
                </Block>
                <Block style={{ paddingBottom: -HeaderHeight * 2 }}>
                  <Block row space="between" style={{ flexWrap: "wrap" }}>
                    {Images.Viewed.map((img, imgIndex) => (
                      <Image
                        source={{ uri: img }}
                        key={`viewed-${img}`}
                        resizeMode="cover"
                        style={styles.thumb}
                      />
                    ))}
                  </Block>
                </Block>
              </Block>
            </Block>
          </ScrollView>
        </ImageBackground>
      </Block>
    </Block>
  );
}

export default Profile 

const styles = StyleSheet.create({
profile: {
  marginTop: Platform.OS === "android" ? -HeaderHeight : 0,
  // marginBottom: -HeaderHeight * 2,
  flex: 1
},
profileContainer: {
  width: width,
  height: height,
  padding: 0,
  zIndex: 1
},
profileBackground: {
  width: width,
  height: height / 2
},
profileCard: {
  // position: "relative",
  padding: theme.SIZES.BASE,
  marginHorizontal: theme.SIZES.BASE,
  marginTop: 165,
  borderTopLeftRadius: 6,
  borderTopRightRadius: 6,
  backgroundColor: theme.COLORS.WHITE,
  shadowColor: "black",
  shadowOffset: { width: 0, height: 0 },
  shadowRadius: 8,
  shadowOpacity: 0.2,
  zIndex: 2
},
info: {
  paddingHorizontal: 40
},
avatarContainer: {
  position: "relative",
  marginTop: -80
},
avatar: {
  width: 124,
  height: 124,
  borderRadius: 62,
  borderWidth: 0
},
nameInfo: {
  marginTop: 5
},
divider: {
  width: "90%",
  borderWidth: 1,
  borderColor: "#E9ECEF"
},
thumb: {
  borderRadius: 4,
  marginVertical: 4,
  alignSelf: "center",
  width: thumbMeasure,
  height: thumbMeasure
}
});


