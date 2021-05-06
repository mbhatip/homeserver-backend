import React, {Component} from 'react'

class Form extends Component {
    constructor(props) {
        super(props);
        this.state = {
            name: '',
            job: '',
        }
        this.handleChange = this.handleChange.bind(this)
    }
    handleChange(event) {
        const {name, value} = event.target

        this.setState({
            [name]: value,
        })
    }
    render() {
        const {name, job} = this.state;
        return (
            <form>
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  name="name"
                  id="name"
                  value={name}
                  onChange={this.handleChange} />
                <label htmlFor="job">Job</label>
                <input
                  type="text"
                  name="job"
                  id="job"
                  value={job}
                  onChange={this.handleChange} />
                <input
                  type="button"
                  value="Submit"
                  onClick={() => {
                      this.props.handleSubmit(this.state)
                      this.setState({name: '', job: ''})
                  }} />
            </form>

        )
    }
}

export default Form;