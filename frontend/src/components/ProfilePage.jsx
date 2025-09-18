import { changePassword, profile, updateUser, deleteUser } from "../api";
import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
// import React, { useEffect } from "react";
export default ProfilePage;
import './ProfilePage.css';


function ProfilePage(){
    const [user, setUser] = useState(null);
    // Update profile states
    const [updateUsername, setUpdateUsername] = useState("");
    const [updateEmail, setUpdateEmail] = useState("");
    const [updateMessage, setUpdateMessage] = useState("");
    const [updateError, setUpdateError] = useState("");
    const [isUpdating, setIsUpdating] = useState(false);
// Change password states
    const [old_password, setOldPassword] = useState("");
    const [new_password, setNewPassword] = useState("");
    const [changePassMessage, setChangePassMessage] = useState("");
    const [changePassError, setChangePassError] = useState("");
    const [isChangingPassword, setIsChangingPassword] = useState(false);

     // Delete account toggle
    const [isDeleting, setIsDeleting] = useState(false);

    const [error, setError] = useState("");
    const navigate = useNavigate();

    // Fetch profile on mount
    useEffect(()=> {
        const fetchUser = async () => {
            try{
                const data = await profile(); //axios GET with jwt
                setUser(data);
            }
            catch (err){
                setError(err.error || "failed to fetch profile")
                localStorage.removeItem("token") //clear jwt if unauthorized
                navigate("/login") //redirect to login
            }
        }
        fetchUser();
    }, [])

    if(error) return <p>Error: {error}</p>
    if(!user) return <p>Loading...</p>;

     // Handlers
    const handleUpdateSubmit = async (e) => {
        e.preventDefault();
        try {
            const data = await updateUser({ username: updateUsername, email: updateEmail });
            setUser(data);
            setUpdateMessage("Profile updated successfully!");
            setUpdateError("");
            setIsUpdating(false);
        } catch (err) {
            setUpdateError(err.error || "Failed to update profile");
            setUpdateMessage("");
        }
    };

    const handleChangePasswordSubmit = async (e) => {
        e.preventDefault();
        try {
            await changePassword({ old_password, new_password });
            setChangePassMessage("Password changed successfully!");
            setChangePassError("");
            setOldPassword("");
            setNewPassword("");
            setIsChangingPassword(false);
        } catch (err) {
            setChangePassError(err.error || "Failed to change password");
            setChangePassMessage("");
        }
    };

    const handleDeleteUser = async () => {
        if (window.confirm("Are you sure you want to delete your account?")) {
            try {
                await deleteUser();
                localStorage.removeItem("token");
                navigate("/login");
            } catch (err) {
                alert(err.error || "Failed to delete account");
            }
        }
    };

    
    return (
        <div className="profile-card" style={{ padding: "20px", maxWidth: "400px", margin: "20px auto", border: "1px solid #ccc", borderRadius: "8px" }}>
            <h2>Profile</h2>
            <p><strong>Username:</strong> {user.username}</p>
            <p><strong>Email:</strong> {user.email}</p>

            {/* Update Profile */}
            <button onClick={() => setIsUpdating(!isUpdating)}>
                {isUpdating ? "Cancel Update" : "Update Profile"}
            </button>
            {isUpdating && (
                <form onSubmit={handleUpdateSubmit} style={{ marginTop: "10px" }}>
                    <input
                        type="text"
                        placeholder="Username"
                        value={updateUsername}
                        onChange={e => setUpdateUsername(e.target.value)}
                        style={{ display: "block", marginBottom: "8px", width: "100%", padding: "8px" }}
                    />
                    <input
                        type="email"
                        placeholder="Email"
                        value={updateEmail}
                        onChange={e => setUpdateEmail(e.target.value)}
                        style={{ display: "block", marginBottom: "8px", width: "100%", padding: "8px" }}
                    />
                    <button type="submit" className="update">Save</button>
                    {updateMessage && <p style={{ color: "green" }}>{updateMessage}</p>}
                    {updateError && <p style={{ color: "red" }}>{updateError}</p>}
                </form>
            )}

            {/* Change Password */}
            <button onClick={() => setIsChangingPassword(!isChangingPassword)} style={{ marginTop: "15px" }}>
                {isChangingPassword ? "Cancel Change Password" : "Change Password"}
            </button>
            {isChangingPassword && (
                <form onSubmit={handleChangePasswordSubmit} style={{ marginTop: "10px" }}>
                    <input
                        type="password"
                        placeholder="Old Password"
                        value={old_password}
                        onChange={e => setOldPassword(e.target.value)}
                        style={{ display: "block", marginBottom: "8px", width: "100%", padding: "8px" }}
                    />
                    <input
                        type="password"
                        placeholder="New Password"
                        value={new_password}
                        onChange={e => setNewPassword(e.target.value)}
                        style={{ display: "block", marginBottom: "8px", width: "100%", padding: "8px" }}
                    />
                    <button type="submit" className="password">Change Password</button>
                    {changePassMessage && <p style={{ color: "green" }}>{changePassMessage}</p>}
                    {changePassError && <p style={{ color: "red" }}>{changePassError}</p>}
                </form>
            )}

            {/* Delete Account */}
            <button className="delete" onClick={handleDeleteUser} style={{ marginTop: "15px", backgroundColor: "red", color: "white" }}>
                Delete Account
            </button>
        </div>
            
    )
}
