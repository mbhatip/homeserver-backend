import React, {Component} from 'react'
import Table from './Table'
import Form from './Form'

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            characters: [
            ]
        }
        this.removeCharacter = this.removeCharacter.bind(this)
    }
    removeCharacter(i) {
        this.setState({
            characters: this.state.characters.filter((char, j) => {
                return i !== j
            })
        })
    }
    
    render() {
        return (
            <div className="container">
                <Table
                    characters={this.state.characters}
                    remove={this.removeCharacter}
                />
                <Form
                    handleSubmit={(char) => {
                        this.setState({characters: [...this.state.characters, char]})
                    }}
                />
            </div>
        )
    }
}

export default App