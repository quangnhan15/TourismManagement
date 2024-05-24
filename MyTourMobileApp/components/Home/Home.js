import { View, Text } from "react-native";
import MyStyles from "../../styles/MyStyles";
import Styles from "./Styles";


const Home = () => {
    return (
        <View style={MyStyles.container}>
            <Text style={Styles.subject}>Home</Text>
        </View>
    )
}

export default Home 