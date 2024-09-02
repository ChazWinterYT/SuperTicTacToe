import React from 'react';

const Version = () => {
    const version = process.env.REACT_APP_VERSION || 'Unknown Version';

    return (
        <div className='Version'>
            Version: {version}
        </div>
    );
};

export default Version;
