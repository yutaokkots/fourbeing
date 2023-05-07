import PropTypes from 'prop-types'

export default function Postcard({ post }) {

  return (
    
    <>
        <div>Postcard</div>
        <h1>{ post.id }</h1>
        <h1>{ post.name }</h1>
        <h1>{ post.description }</h1>
    </>
  )
}

Postcard.propTypes = {
  post: PropTypes.object.isRequired
}